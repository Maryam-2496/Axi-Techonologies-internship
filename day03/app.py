from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Maryam", "email": "maryam@example.com"},
    {"id": 2, "name": "Sara", "email": "sara@example.com"},
    {"id": 3, "name": "ali", "email": "ali@example.com"},

]
next_id = 4

# CREATE
@app.route("/users", methods=["POST"])
def create_user():
    global next_id
    data = request.json
    new_user = {"id": next_id, "name": data.get("name"), "email": data.get("email")}
    users.append(new_user)
    next_id += 1
    return jsonify(new_user), 201

# READ
@app.route("/users", methods=["GET"])
def get_all_users():
    return jsonify(users)

@app.route("/users/<int:id>", methods=["GET"])
def get_single_user(id):
    for user in users:
        if user["id"] == id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

#UPDATE
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    for user in users:
        if user["id"] == id:
            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

#DELETE
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    global users
    for user in users:
        if user["id"] == id:
            users = [u for u in users if u["id"] != id]
            return jsonify({"message": f"User {id} deleted"})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(port=3000, debug=True)