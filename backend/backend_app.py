from flask import Flask, jsonify, request
from flask_cors import CORS
from isort.api import sort_file

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "The Scribe of god", "content": "I am Metatron. I am called the Scribe of God. Don't mess with me!"},
    {"id": 2, "title": "Dean Winchester", "content": "I am Dean. Don't mess with me and please don't forget: I'm a human after all!"},
    {"id": 3, "title": "Jack", "content": "I'll make everything ok!"},
    {"id": 4, "title": "Castiel", "content": "I try to be the new god; strong!"},
    {"id": 5, "title": "Sam Winchester", "content": "I'm Sam. I'll take care of all of the above characters :D"}
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
    sort_query = request.args.get("sort")
    direction_query = request.args.get("direction")

    if sort_query and sort_query not in ["title", "content"]:
        return jsonify({"error": f"Invalid sort field: {sort_query}. Allowed: title, content"}), 400

    if direction_query and direction_query not in ["asc", "desc"]:
        return jsonify({"error": f"Invalid direction: {direction_query}. Allowed: asc, desc"}), 400

    results = POSTS

    if sort_query:
        is_desc = (direction_query == "desc")
        results = sorted(POSTS, key=lambda post: post[sort_query].lower(), reverse=is_desc)

    return jsonify(results), 200


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


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global POSTS

    if id not in [post["id"] for post in POSTS]:
        return jsonify({"message": f"There is no Post with id {id}."}), 404

    POSTS = [post for post in POSTS if post['id'] != id]

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


def fetch_post_by_id(post_id):
    """Searches for a post using its ID"""
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = fetch_post_by_id(id)
    if post is None:
        return jsonify({"message": f"There is no Post with id {id}."}), 404

    new_data = request.get_json()

    post["title"] = new_data.get("title", post["title"])
    post["content"] = new_data.get("content", post["content"])

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get("title")
    content_query = request.args.get("content")

    # lowercase letter ONCE before the loop.
    search_title = title_query.lower() if title_query else None
    search_content = content_query.lower() if content_query else None

    results = [post for post in POSTS
               if (title_query and search_title in post["title"].lower())
               or (content_query and search_content in post["content"].lower())
               ]

    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
