from flask import Blueprint, jsonify, request
from returns.maybe import Maybe
from returns.result import Success

from repositories.database_repository import init_db_with_indexes
from repositories.injury_repository import get_injury_by_region, get_injury_reason_by_region, get_injury_statistic, \
    get_injury_by_month_and_region, get_injury_by_date_and_region, get_injuries_in_week_from_date_and_region

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


@injury_blueprint.route('/get_injury_by_month_and_region/<string:month>/<string:region>', methods=['GET'])
def get_injury_by_month_and_region_api(month: str, region: str):
    res = get_injury_by_month_and_region(month, region)

    return jsonify(res), 200


@injury_blueprint.route('/get_injury_by_date_and_region/<string:region>', methods=['GET'])
def get_injury_by_date_and_region_api(region: str):
    date = request.args.get('date', type=str)
    res = get_injury_by_date_and_region(date, region)
    return jsonify(res), 200


@injury_blueprint.route('/get_injuries_in_week_from_date_and_region/<string:region>', methods=['GET'])
def get_injuries_in_week_from_date_and_region_api(region: str):
    start_date = request.args.get('date', type=str)
    res = get_injuries_in_week_from_date_and_region(start_date, region)
    return jsonify({f"injuries": res}), 200


@injury_blueprint.route('/init', methods=['GET'])
def get_injuries_in_week_from_date_and_region_api():
    init_db_with_indexes()
    return jsonify({"message": "success"}), 200
