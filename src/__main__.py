# __main__.py

import argparse
import sys
from dotenv import load_dotenv
from requester import Requester


def main() -> None:
    parser = argparse.ArgumentParser(
                        prog='NVidiallamaTest',
                        description='Playing with the NV code llama endpoints',
                        epilog='Enjoy!')
    parser.add_argument('-s', '--session', dest='endpoint', action='store_const',
                        const=Requester.session_endpoint, default=Requester.stream_endpoint,
                        help='GET using session (default: stream)')
    parser.add_argument('-q', '--query', type=str,
                        default=None,
                        help='query to the model (default: fibonacci)')

    args = parser.parse_args()

    load_dotenv()  # take environment variables from .env.
    #  Requester.stream_endpoint()
    args.endpoint(args.query)


if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
    main()
