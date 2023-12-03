# requester.py

from typing import Optional
import requests
import os

invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/df2bee43-fb69-42b9-9ee5-f4eabbeaf3a8"
fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"
default_query = "Write the Fibonacci sequence in Python"

class Requester:
    @classmethod
    def __get_payload_json(cls, stream: bool, query: Optional[str] = None) -> dict:
        payload = {
        "messages": [
            {
            "content": query if query is not None else default_query,
            "role": "user"
            }
        ],
        "temperature": 0.2,
        "top_p": 0.7,
        "max_tokens": 1024,
        "stream": stream
        }
        return payload

    @classmethod
    def __get_api_key_authorization(cls) -> dict:
        API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC = os.getenv("NV_API_KEY")
        return { "Authorization": f"Bearer {API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC}" }

    @classmethod
    def session_endpoint(cls, query: Optional[str] = None) -> None:
        headers = {
            **cls.__get_api_key_authorization(),
            "Accept": "application/json",
        }
        payload = cls.__get_payload_json(False, query)

        # re-use connections
        session = requests.Session()

        response = session.post(invoke_url, headers=headers, json=payload)

        while response.status_code == 202:
            request_id = response.headers.get("NVCF-REQID")
            fetch_url = fetch_url_format + request_id
            response = session.get(fetch_url, headers=headers)

        response.raise_for_status()
        response_body = response.json()
        print(response_body)
    
    def stream_endpoint(cls, query: Optional[str] = None) -> None:
        headers = {
            **cls.__get_api_key_authorization(),
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }
        payload = cls.__get_payload_json(True, query)

        response = requests.post(invoke_url, headers=headers, json=payload, stream=True)

        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))

Requester.stream_endpoint = classmethod(Requester.stream_endpoint)