# api/v1/views/places_amenities.py
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage, Place, Amenity

@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST', 'DELETE'])
def place_amenities(place_id):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)

    if request.method == 'POST':
        amenity_id = request.args.get('amenity_id')
        if amenity_id is None:
            abort(400, "Missing amenity_id")

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201

    if request.method == 'DELETE':
        amenity_id = request.args.get('amenity_id')
        if amenity_id is None:
            abort(400, "Missing amenity_id")

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
        place.save()
        return jsonify({}), 200


