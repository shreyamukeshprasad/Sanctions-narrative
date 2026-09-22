from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import os
import httpx
import json

load_dotenv()

SECRET_SCOPE = "llm-secrets"
SECRET_KEY = "api-key"


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


def get_databricks_secret(scope: str, key: str) -> str | None:
    try:
        from databricks.sdk import WorkspaceClient

        client = WorkspaceClient()
        return client.secrets.get_secret(scope=scope, key=key).value
    except Exception as exc:
        print(f"Unable to read Databricks secret {scope}/{key}: {exc}")
        return None


def create_llm():
    model = os.getenv("MODEL")
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY") or get_databricks_secret(SECRET_SCOPE, SECRET_KEY)

    missing = [
        name
        for name, value in {
            "MODEL": model,
            "BASE_URL": base_url,
            "API_KEY": api_key,
        }.items()
        if not value
    ]

    if missing:
        raise RuntimeError(f"Missing required LLM environment variables: {', '.join(missing)}")

    return ChatOpenAI(
        model=model,
        max_tokens=None,
        base_url=base_url,
        api_key=api_key,
        http_client=http_client,
    )


def ask_llm(prompt: str) -> str:
    llm = create_llm()
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    response = ask_llm("Hello, this is a test")

    print("\nRESPONSE:")
    print(response)
