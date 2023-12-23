from typing import Any, Dict
from starlette.testclient import TestClient


def post_request(
    client: TestClient,
    url: str,
    json: Dict[str, Any] = {},
    data: Dict[str, Any] = {},
    headers: Dict[str, Any] = {},
) -> Any:  # sourcery skip: default-mutable-arg
    response = client.post(url, headers=headers, json=json, data=data)
    return response.json()


def get_request(
    client: TestClient,
    url: str,
    headers: Dict[str, Any] = {},
) -> Any:  # sourcery skip: default-mutable-arg
    response = client.get(url=url, headers=headers)
    return response.json()


def put_request(
    client: TestClient,
    url: str,
    payload: Dict[str, Any],
    headers: Dict[str, Any] = {},
) -> Any:  # sourcery skip: default-mutable-arg
    response = client.put(url=url, json=payload, headers=headers)
    return response.json()


def delete_request(
    client: TestClient,
    url: str,
    headers: Dict[str, Any] = {},
) -> Any:  # sourcery skip: default-mutable-arg
    response = client.delete(url=url, headers=headers)
    return response.json()
