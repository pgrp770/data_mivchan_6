import pytest
from flask import Flask
from controllers.injury_controller import injury_blueprint


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(injury_blueprint)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_injury_statistic_api(client):
    response = client.get('/get_injury_statistic/225')
    assert response.status_code == 200


def test_get_injury_reason_by_region_api(client):
    response = client.get('/get_injury_reason_by_region/225')
    assert response.status_code == 200


def test_get_injury_by_region_api(client):
    response = client.get('/get_injury_by_region/225')
    assert response.status_code == 200


def test_get_injury_by_month_and_region_api(client):
    response = client.get('get_injury_by_month_and_region/02/1652')
    assert response.status_code == 200


def test_get_injury_by_date_and_region_api(client):
    response = client.get('/get_injury_by_date_and_region/225?date=09/05/2023')
    assert response.status_code == 200


def test_get_injuries_in_week_from_date_and_region_api(client):
    response = client.get('/get_injuries_in_week_from_date_and_region/225?date=09/05/2023')
    assert response.status_code == 200
