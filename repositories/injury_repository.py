from datetime import datetime, timedelta

from returns.maybe import Maybe
from returns.result import Result, Success, Failure
from pymongo.errors import PyMongoError
from database.connect import region_injuries, region_cause_of_death, daily_injuries, monthly_injuries
from toolz import *

def get_injury_by_region(region: str) -> Result:
    try:

        res = region_injuries.find_one(
            {'region': region},
            {'_id': 0, 'injuries_total': 1}
        )
        if res:
            return Success(res)
        return Failure("404")
    except PyMongoError as ex:
        return Failure(str(ex))


def get_injury_reason_by_region(region: str):
    return Maybe.from_optional(region_cause_of_death.find_one({"region": region}))


def get_injury_statistic(region: str):
    return region_injuries.find_one(
        {'region': region},
    )


def get_injury_by_month_and_region(month: str, region: str):
    document = monthly_injuries.find_one({"month": month})

    for region_injury in document.get("region_injuries", []):
        if region_injury.get("region") == region:
            return region_injury

    return None


def get_injury_by_date_and_region(date: str, region: str):
    document = daily_injuries.find_one({"date": date})
    if not document:
        return None
    res = next(filter(lambda a: a["region"] == region, document['region_injuries']))
    if res:
        return res
    return None


def get_injuries_in_week_from_date_and_region(start_date: str, region: str):
    start_date_obj = datetime.strptime(start_date, "%m/%d/%Y")
    end_date_obj = start_date_obj + timedelta(days=7)
    start_date_str = start_date_obj.strftime("%m/%d/%Y")
    end_date_str = end_date_obj.strftime("%m/%d/%Y")
    documents = daily_injuries.find({"date": {"$gte": start_date_str, "$lte": end_date_str}})

    return pipe(
        documents,
        partial(map, lambda document: document["region_injuries"]),
        partial(map, lambda a: filter(lambda x: x["region"] == region, a)),
        partial(map, lambda a: list(a)),
        partial(filter, lambda a: a),
        partial(map, lambda a: a[0]),
        partial(map, lambda a: a["injuries_total"]),
        list,
        sum

    )
