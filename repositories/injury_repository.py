from datetime import datetime, timedelta

from database.connect import region_injuries, region_cause_of_death, daily_injuries, monthly_injuries


def get_injury_by_region(region: str):
    return region_injuries.find_one(
        {'region': region},
        {'_id': 0, 'injuries_total': 1}
    )


def get_injury_reason_by_region(region: str):
    return region_cause_of_death.find_one({"region": region})


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

    for region_injury in document.get("region_injuries", []):
        if region_injury.get("region") == region:
            return region_injury

    return None


def get_injuries_in_week_from_date_and_region(start_date: str, region: str):
    start_date_obj = datetime.strptime(start_date, "%m/%d/%Y")
    end_date_obj = start_date_obj + timedelta(days=7)
    start_date_str = start_date_obj.strftime("%m/%d/%Y")
    end_date_str = end_date_obj.strftime("%m/%d/%Y")
    documents = daily_injuries.find({"date": {"$gte": start_date_str, "$lte": end_date_str}})
    total_injuries = 0
    for document in documents:
        for region_injury in document.get("region_injuries", []):
            if region_injury.get("region") == region:
                total_injuries += region_injury.get("injuries_total", 0)
    return total_injuries
