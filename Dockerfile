FROM python:3.11
WORKDIR /app
COPY ./main /app/main
COPY ./test /app/test
COPY ./requirements.txt /app
#WORKDIR /main
#RUN mkdir /main/logs
RUN apt-get update
RUN mkdir /app/data
RUN mkdir /app/data/sqlite3
RUN touch /app/data/sqlite3/events.db
RUN touch app.log
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#EXPOSE 5432
CMD ["python", "main/real_init.py"]