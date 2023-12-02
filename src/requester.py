# requester.py

import requests
import os

invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/df2bee43-fb69-42b9-9ee5-f4eabbeaf3a8"

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
  "stream": True
}

class Requester:
    def ask_endpoint(cls) -> None:
        API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC = os.getenv("NV_API_KEY")
        headers = {
            "Authorization": f"Bearer {API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC}",
            "accept": "text/event-stream",
            "content-type": "application/json",
        }

        response = requests.post(invoke_url, headers=headers, json=payload, stream=True)

        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))

Requester.ask_endpoint = classmethod(Requester.ask_endpoint)