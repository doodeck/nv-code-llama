# requester.py

import requests
import os

invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/df2bee43-fb69-42b9-9ee5-f4eabbeaf3a8"
fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"

payload = {
  "messages": [
    {
      "content": "Write the Fibonacci sequence in Python",
      "role": "user"
    }
  ],
  "temperature": 0.2,
  "top_p": 0.7,
  "max_tokens": 1024,
  # "stream": True
}

class Requester:
    @classmethod
    def session_endpoint(cls) -> None:
        API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC = os.getenv("NV_API_KEY")
        headers = {
            "Authorization": f"Bearer {API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC}",
            "Accept": "application/json",
        }
        payload["stream"] = False

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
    
    def stream_endpoint(cls) -> None:
        API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC = os.getenv("NV_API_KEY")
        headers = {
            "Authorization": f"Bearer {API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC}",
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }
        payload["stream"] = True

        response = requests.post(invoke_url, headers=headers, json=payload, stream=True)

        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))

Requester.stream_endpoint = classmethod(Requester.stream_endpoint)