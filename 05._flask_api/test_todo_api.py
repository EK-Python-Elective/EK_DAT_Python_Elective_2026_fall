"""Demo 3: test en Flask API uden at starte en server.

Kør:
    uv run --with flask --with pytest pytest test_todo_api.py -v
"""

import pytest

import todo_api


@pytest.fixture
def client():
    todo_api.todos.clear()          # frisk tilstand for hver test
    todo_api.next_id = 1
    return todo_api.app.test_client()


def test_list_is_empty_at_start(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_todo(client):
    response = client.post("/todos", json={"title": "Lær Flask"})
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "title": "Lær Flask", "done": False}


def test_create_todo_without_title_fails(client):
    response = client.post("/todos", json={})
    assert response.status_code == 400


def test_unknown_todo_returns_404(client):
    response = client.get("/todos/99")
    assert response.status_code == 404
    assert response.get_json() == {"error": "ikke fundet"}
