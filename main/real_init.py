import time
import logging

# Wait until user connects to docker container CLI and stop container.
# Exist not to make python app container dead & interact at CLI.
if __name__ == '__main__':
    try:
        while True:  # Keep the main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Exit Program by KeyboardInterrupt.")