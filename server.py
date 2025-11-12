from flask import Flask, request, jsonify, abort, make_response, url_for

#!/usr/bin/env python3

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# In-memory store for demo purposes
_items = {}
_next_id = 1


def _generate_id():
    global _next_id
    _next_id += 1
    return _next_id - 1


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Basic Flask REST API", "endpoints": ["/items"]})


@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(list(_items.values()))


@app.route("/items", methods=["POST"])
def create_item():
    if not request.is_json:
        return make_response(jsonify({"error": "Request body must be JSON"}), 415)
    payload = request.get_json()
    if not isinstance(payload, dict) or "name" not in payload:
        return make_response(jsonify({"error": "JSON must contain 'name' field"}), 400)
    item_id = _generate_id()
    item = {
        "id": item_id,
        "name": payload.get("name"),
        "description": payload.get("description", ""),
    }
    _items[item_id] = item
    resp = make_response(jsonify(item), 201)
    resp.headers["Location"] = url_for("get_item", item_id=item_id, _external=False)
    return resp


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int):
    item = _items.get(item_id)
    if item is None:
        abort(404)
    return jsonify(item)


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id: int):
    if not request.is_json:
        return make_response(jsonify({"error": "Request body must be JSON"}), 415)
    if item_id not in _items:
        abort(404)
    payload = request.get_json()
    if not isinstance(payload, dict):
        return make_response(jsonify({"error": "Invalid JSON body"}), 400)
    item = _items[item_id]
    # Allow updating name and description
    if "name" in payload:
        item["name"] = payload["name"]
    if "description" in payload:
        item["description"] = payload["description"]
    _items[item_id] = item
    return jsonify(item)


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id: int):
    if item_id not in _items:
        abort(404)
    del _items[item_id]
    return "", 204


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(e):
    return make_response(jsonify({"error": "Bad request"}), 400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)