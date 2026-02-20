from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    errors = []
    if not data:
        return {"error": "No data provided"}, 400

    if "title" not in data or not data["title"].strip():
        errors.append("title is required")

    if "content" not in data or not data["content"].strip():
        errors.append("content is required")

    if errors:
        return {"errors": "Invalid data", "missing_fields": errors}, 400

    return None, 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post_data = request.get_json()

    error_message, status_code = validate_post_data(new_post_data)
    if error_message:
        return jsonify(error_message), status_code

    # Generate a new ID for the post
    new_id = max([post["id"] for post in POSTS], default=0) + 1

    new_post = {
        "id": new_id,
        "title": new_post_data["title"],
        "content": new_post_data["content"]
    }

    # Add the new book to our list
    POSTS.append(new_post)

    # Return the new book data to the client
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
