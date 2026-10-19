"""Demo 1: den mindste mulige Flask API.

Kør:
    uv run --with flask python hello_api.py

Prøv i Postman (GET):
    http://127.0.0.1:5000/
    http://127.0.0.1:5000/hello/Alice
    http://127.0.0.1:5000/add?a=2&b=3
    http://127.0.0.1:5000/users
    http://127.0.0.1:5000/users/2

Prøv i Postman (POST) med Body -> raw -> JSON:
    http://127.0.0.1:5000/users
    {"name": "Dave", "email": "dave@example.com"}

Prøv i Postman (PUT) med Body -> raw -> JSON:
    http://127.0.0.1:5000/users/2
    {"name": "Bobby", "email": "bobby@example.com"}

Prøv i Postman (DELETE):
    http://127.0.0.1:5000/users/2
"""

from flask import Flask, request

app = Flask(__name__)

# "Database": en liste af dicts, der lever i hukommelsen (forsvinder ved genstart)
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
]


@app.get("/")                          # route: GET /
def index():
    return {"message": "Hej fra Flask!"}   # en dict bliver automatisk til JSON


@app.get("/hello/<name>")              # path-parameter: /hello/Alice
def hello(name):
    return {"greeting": f"Hej, {name}!"}


@app.get("/add")                       # query-parametre: /add?a=2&b=3
def add():
    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    if a is None or b is None:
        return {"error": "a og b skal være heltal"}, 400   # (body, statuskode)
    return {"result": a + b}


@app.get("/users")                     # hent alle
def get_users():
    return users                       # en liste bliver også til JSON


@app.get("/users/<int:user_id>")       # <int:...> konverterer til int: /users/2
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": f"Ingen bruger med id {user_id}"}, 404


@app.post("/users")                    # route: POST /users med JSON-body
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return {"error": "name og email er påkrævet"}, 400
    new_user = {
        "id": max((u["id"] for u in users), default=0) + 1,
        "name": data["name"],
        "email": data["email"],
    }
    users.append(new_user)
    return new_user, 201               # 201 Created


@app.put("/users/<int:user_id>")       # route: PUT /users/2 med JSON-body
def update_user(user_id):
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return {"error": "name og email er påkrævet"}, 400
    for user in users:
        if user["id"] == user_id:
            user["name"] = data["name"]    # dicts er mutable: vi ændrer direkte i listen
            user["email"] = data["email"]
            return user
    return {"error": f"Ingen bruger med id {user_id}"}, 404


@app.delete("/users/<int:user_id>")    # route: DELETE /users/2
def delete_user(user_id):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return "", 204             # 204 No Content: succes, men ingen body
    return {"error": f"Ingen bruger med id {user_id}"}, 404


if __name__ == "__main__":
    app.run(debug=True)                # debug=True: auto-reload når du gemmer filen
