import logging


# Configure the root logger
def setLogOptions():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app.log',  # Specify the file name for file-based logging (optional)
    )

    # Add additional logging options (optional)
    # Adding a console handler to display logs on the console as well
    # TODO: handler 종류 알아 보기
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set the desired logging level for the console handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Attach the console handler to the root logger
    logging.getLogger('').addHandler(console_handler)