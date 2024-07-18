from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture is not None:
        return jsonify(picture)
    else:
        return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    existing_picture = next((item for item in data if item["id"] == picture["id"]), None)
    if existing_picture is not None:
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
    data.append(picture)
    res = make_response(jsonify(picture))
    res.status_code = 201
    return res

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract the picture data from the request body
    picture_data = request.json
    
    # Find the picture in the data list
    picture_index = next((index for (index, item) in enumerate(data) if item["id"] == id), None)
    
    if picture_index is None:
        # If the picture with the given ID does not exist, return 404 with a message
        return jsonify({"message": "picture not found"}), 404
    
    # Update the picture with the new data
    data[picture_index] = {**data[picture_index], **picture_data}
    
    # Return the updated picture with a 200 status code
    return jsonify(data[picture_index]), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture index in the data list
    picture_index = next((index for (index, item) in enumerate(data) if item["id"] == id), None)
    
    if picture_index is None:
        # If the picture with the given ID does not exist, return 404 with a message
        return jsonify({"message": "picture not found"}), 404
    
    # Remove the picture from the data list
    data.pop(picture_index)
    
    # Return an empty response with 204 No Content status
    return '', 204
