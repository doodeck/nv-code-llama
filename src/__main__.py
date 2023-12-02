# __main__.py

from dotenv import load_dotenv
from requester import Requester

def main() -> None:
    load_dotenv()  # take environment variables from .env.
    Requester.ask_endpoint()


if __name__ == "__main__":
    main()
