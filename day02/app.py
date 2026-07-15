from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Day 02!"

@app.route("/search")
def search():
    query = request.args.get("query")
    return jsonify({"you_searched_for": query})

@app.route("/users/<int:id>")
def get_user(id):
    return jsonify({"user_id": id, "message": f"You asked for user number {id}"})

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    return jsonify({
        "message": "User created successfully",
        "name": name,
        "email": email
    }), 201

if __name__ == "__main__":
    app.run(port=3000, debug=True)