from flask import Blueprint, jsonify, request
from returns.maybe import Maybe
from returns.result import Success
from repositories.injury_repository import get_injury_by_region, get_injury_reason_by_region, get_injury_statistic
from bson import ObjectId

injury_blueprint = Blueprint('car', __name__)


@injury_blueprint.route('/get_injury_by_region/<string:region>', methods=['GET'])
def get_injury_by_region_api(region: str):
    res = get_injury_by_region(region)
    return jsonify(res), 200


@injury_blueprint.route('/get_injury_reason_by_region/<string:region>', methods=['GET'])
def get_injury_reason_by_region_api(region: str):
    res = get_injury_reason_by_region(region)
    res["_id"] = str(res["_id"])
    return jsonify(res), 200


@injury_blueprint.route('/get_injury_statistic/<string:region>', methods=['GET'])
def get_injury_statistic_api(region: str):
    res = get_injury_statistic(region)
    res["_id"] = str(res["_id"])
    return jsonify(res), 200
