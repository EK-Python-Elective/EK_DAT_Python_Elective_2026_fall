"""Demo 2: en CRUD API med Flask — todos gemt i hukommelsen.

Kør:
    uv run --with flask python todo_api.py

Prøv i en anden terminal (Git Bash / macOS / Linux):
    curl http://127.0.0.1:5000/todos
    curl -X POST http://127.0.0.1:5000/todos -H "Content-Type: application/json" -d '{"title": "Lær Flask"}'
    curl http://127.0.0.1:5000/todos/1
    curl -X PUT http://127.0.0.1:5000/todos/1 -H "Content-Type: application/json" -d '{"done": true}'
    curl -X DELETE http://127.0.0.1:5000/todos/1
    curl -i http://127.0.0.1:5000/todos/99          # -i viser statuskoden (404)
"""

from flask import Flask, abort, request

app = Flask(__name__)

todos = {}      # id -> todo (forsvinder når serveren genstartes)
next_id = 1


@app.get("/todos")
def list_todos():
    return list(todos.values())                 # en liste bliver også til JSON


@app.get("/todos/<int:todo_id>")                # <int:...> konverterer og validerer
def get_todo(todo_id):
    if todo_id not in todos:
        abort(404)
    return todos[todo_id]


@app.post("/todos")
def create_todo():
    global next_id
    data = request.get_json(silent=True) or {}  # None hvis body ikke er JSON
    title = data.get("title")
    if not title:
        return {"error": "title er påkrævet"}, 400
    todo = {"id": next_id, "title": title, "done": False}
    todos[next_id] = todo
    next_id += 1
    return todo, 201                            # 201 Created


@app.put("/todos/<int:todo_id>")
def update_todo(todo_id):
    if todo_id not in todos:
        abort(404)
    data = request.get_json(silent=True) or {}
    todo = todos[todo_id]
    todo["title"] = data.get("title", todo["title"])
    todo["done"] = data.get("done", todo["done"])
    return todo


@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    if todos.pop(todo_id, None) is None:
        abort(404)
    return "", 204                              # 204 No Content


@app.errorhandler(404)
def not_found(error):
    return {"error": "ikke fundet"}, 404       # JSON i stedet for Flasks HTML-fejlside


if __name__ == "__main__":
    app.run(debug=True)
