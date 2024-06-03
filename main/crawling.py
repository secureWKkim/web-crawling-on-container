import requests
import datetime
from bs4 import BeautifulSoup
import logging

from connect_cache import return_sqlite_conn


def scraping_html(response):
    data_to_cache = []

    # TODO: nested div-class 에서 find, select 다 안 먹히는 경우 대체 어케해야 하는지. 원했던 데이터 더 갖고 오기
    soup = BeautifulSoup(response.text, 'html.parser')
    to_be_parsed = soup.select_one("#main-container > div > div > div > div > div > div > div")

    for se in to_be_parsed:
        # TODO: improve performance by not using some str util methods
        game_schedules = se.get_text(strip=True).split("•")
        logging.debug(game_schedules)
        game_date = game_schedules.pop(0)
        if game_date.startswith('Today'):
            current_timestamp = datetime.date.today().strftime('%Y-%m-%d')
            input_string = "{} {}".format(current_timestamp, game_date[7:])
            data_to_cache.append(
                (" ".join(game_schedules), datetime.datetime.strptime(input_string, "%Y-%m-%d %H:%M %p")))
        elif game_date.startswith('Tomorrow'):
            timestamp = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            input_string = "{} {}".format(timestamp, game_date[10:])
            data_to_cache.append(
                (" ".join(game_schedules), datetime.datetime.strptime(input_string, "%Y-%m-%d %H:%M %p")))
    return []



def crawl_data_to_insert():
    url = "https://www.espncricinfo.com/series/india-in-west-indies-2023-1381201/match-schedule-fixtures-and-results"
    response = requests.get(url)
    if response.status_code != 200:
        # TODO: throw exception then exit
        logging.error("Failed to retrieve the website content.")

    # data_to_cache = []
    cache_to_sqlite3(scraping_html(response))


def cache_to_sqlite3(data_to_cache):
    conn = return_sqlite_conn()
    cursor = conn.cursor()

    # TODO: Check if there's nothing to cache
    cursor.executemany("""
        INSERT INTO events (title, event_time)
            VALUES (?, ?)
            ON CONFLICT(title) DO UPDATE SET event_time = excluded.event_time;
    """, data_to_cache)
    conn.commit()
    logging.info("Successfully cached data to write in DB.")
    conn.close()



# trials for better crawling
    # match_elements = soup.select('.js-matchlist-match')  # This class might change based on the website's structure
    #
    # data_to_store = []
    # for match in match_elements:
    #     match_date = match.select_one('.match-date').text.strip()
    #     match_info = match.select_one('.match-info-link').text.strip()
    #     data_to_store.append((match_date, match_info))
    # c = soup.find_all("span", {"class":"ds-text-tight-s ds-font-medium ds-bg-ui-fill-alternate ds-py-1 ds-px-2 ds-rounded-2xl"}) # 찐 날짠데, 안 갖고와짐 ㅠㅠㅠ
    # a = soup.find_all("span", {"class":"ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5"}) # Today, 4:00 PM OR RESULT
    # b = soup.find_all("div", {"class":"ds-text-tight-s ds-font-regular ds-truncate ds-text-typo-mid3"})
    # for z in zip(a, b):
    #     result_or_date, title = z[0].text.strip(), z[1].text.strip()
    #     print(result_or_date, ': ', title, '\n') #z[2].text,


    # print(soup.select_one("#main-container > div > div > div > div > div > div > div"))
    # 그 네모 단위 핵심인데, 둘중 어떻게 해도 안됨
    # print(soup.select_one("#main-container > div > div > div > div > div > div > div").find_all("span", {"class":"ds-text-tight-s ds-font-medium ds-bg-ui-fill-alternate ds-py-1 ds-px-2 ds-rounded-2xl"}))
    # print(soup.select("#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5 > div.ds-flex.ds-space-x-5 > div > div.ds-mb-4 > div > div > div"))
    # for c in soup.find_all("div", {"class":"ds-bg-fill-content-prime hover:ds-bg-ui-fill-translucent"}):
    #     print(c, '\n')
