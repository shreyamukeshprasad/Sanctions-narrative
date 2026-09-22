# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# import os

# load_dotenv()

# llm = ChatOpenAI(
#     model=os.getenv("MODEL"),
#     max_tokens=None,
#     base_url=os.getenv("BASE_URL"),
#     api_key=os.getenv("API_KEY"),
# )

# response = llm.invoke(input("Hi! I am an AI assistant. Ask me anything! : \n"))

# print(response.content)

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import os
import httpx
import json

load_dotenv()


def log_request(request: httpx.Request):
    print("\n========== OUTGOING REQUEST ==========")
    print("METHOD:")
    print(request.method)

    print("\nURL:")
    print(request.url)

    print("\nHEADERS:")
    for key, value in request.headers.items():
        if key.lower() == "authorization":
            print(f"{key}: Bearer ***HIDDEN***")
        else:
            print(f"{key}: {value}")

    print("\nBODY:")
    try:
        body = json.loads(request.content)
        print(json.dumps(body, indent=2))
    except Exception:
        print(request.content)

    print("======================================\n")


http_client = httpx.Client(
    event_hooks={
        "request": [log_request]
    }
)


llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    max_tokens=None,
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    http_client=http_client,
)


response = llm.invoke("Hello, this is a test")

print("\nRESPONSE:")
print(response.content)