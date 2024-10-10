from repositories.injury_repository import get_injury_by_region, get_injury_reason_by_region, get_injury_statistic, \
    get_injury_by_month_and_region, get_injury_by_date_and_region, \
    get_injuries_in_week_from_date_and_region


def test_get_injury_by_region():
    res = get_injury_by_region("225")
    assert res["injuries_total"] == 115


def test_get_injury_reason_by_region():
    res = get_injury_reason_by_region("225")
    assert res["region"] == "225"


def test_get_injury_statistic():
    res = get_injury_statistic("225")
    assert res["region"] == "225"


def test_get_injury_by_month_and_region():
    res = get_injury_by_month_and_region("02", "1652")
    assert res["region"] == "1652"


def test_get_injury_by_date_and_region():
    res = get_injury_by_date_and_region("09/05/2023", "225")
    assert res["injuries_total"] == 3


def test_get_injuries_in_week_from_date_and_region():
    res = get_injuries_in_week_from_date_and_region("09/05/2023", "225")
    assert res == 13
