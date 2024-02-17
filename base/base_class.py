from dotenv import load_dotenv, find_dotenv


class BaseClass:
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        print("Environment variables loaded.")