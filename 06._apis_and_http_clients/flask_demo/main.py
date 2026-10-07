from flask import Flask, request

app = Flask(__name__)

users = [{'name': 'Claus', 'age' : 33}, {'name': 'Anna', 'age' : 43}]


@app.get('/')
def index():
    return {'msg' : 'Hello'}


@app.get('/users')
def get_users():
    return users, 200

@app.post('/users')
def set_users():
    data = request.get_json()
    new_user = {
        "name": data["name"],
        "age": data["age"]
    }
    users.append(new_user)
    return new_user, 201  

@app.put('/users/<name>')
def change_user(name):
    data = request.get_json()
    for user in users:
        if user['name'] == name:
            user['name'] = data['name']
            user['age'] = data['age']

    return users, 201

@app.delete('/users/<name>')
def remove_user(name):
    for user in users:
        if user['name'] == name:
            users.remove(user)
    return users, 200
    

app.run(port=5001)







    
