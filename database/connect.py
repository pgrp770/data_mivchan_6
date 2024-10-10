from pymongo import MongoClient


client = MongoClient('mongodb://172.20.8.99:27017')

crash_db = client['crash-db']

region_injuries = crash_db['region_injuries']
region_cause_of_death = crash_db['region_cause_of_death']
daily_injuries = crash_db['daily_injuries']
yearly_injuries = crash_db['yearly_injuries']
