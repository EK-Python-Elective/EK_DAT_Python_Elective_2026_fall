"""Demo 1: den mindste mulige Flask API.

Kør:
    uv run --with flask python hello_api.py

Prøv i en anden terminal:
    curl http://127.0.0.1:5000/
    curl http://127.0.0.1:5000/hello/Alice
    curl "http://127.0.0.1:5000/add?a=2&b=3"
"""

from flask import Flask, request

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)                # debug=True: auto-reload når du gemmer filen
