from database.connect import region_injuries, region_cause_of_death, daily_injuries, monthly_injuries
from services.csv_service import read_csv


def init_crash_db(path):
    region_injuries.drop()
    region_cause_of_death.drop()
    daily_injuries.drop()
    monthly_injuries.drop()

    for row in read_csv(path):
        injuries_total = int(row['INJURIES_TOTAL']) if row['INJURIES_TOTAL'].strip() else 0
        fatal_injuries = int(row['INJURIES_FATAL'].strip()) if row['INJURIES_FATAL'].strip() else 0
        non_fatal_injuries = int(row['INJURIES_NON_INCAPACITATING'].strip()) if row[
            'INJURIES_NON_INCAPACITATING'].strip() else 0

        injuries_data = {
            'injuries_total': injuries_total,
            'fatal_injuries': fatal_injuries,
            'non_fatal_injuries': non_fatal_injuries,
            'injuries_list': [
                row['CRASH_TYPE']
            ]
        }

        region_injuries.update_one(
            {'region': row['BEAT_OF_OCCURRENCE']},
            {
                '$inc': {
                    'injuries_total': injuries_total,
                    'fatal_injuries': fatal_injuries,
                    'non_fatal_injuries': non_fatal_injuries
                },
                '$addToSet': {
                    'injuries_list': row['CRASH_TYPE']
                }
            },
            upsert=True
        )

        region_cause_of_death.update_one(
            {'region': row['BEAT_OF_OCCURRENCE']},
            {
                '$inc': {
                    f'causes.{row["PRIM_CONTRIBUTORY_CAUSE"]}': 1
                }
            },
            upsert=True
        )

        daily_injuries.update_one(
            {'date': row['CRASH_DATE'].split()[0], 'region_injuries.region': row['BEAT_OF_OCCURRENCE']},
            {
                '$inc': {
                    'region_injuries.$.injuries_total': injuries_total
                }
            }
        )

        daily_injuries.update_one(
            {'date': row['CRASH_DATE'].split()[0]},
            {
                '$addToSet': {
                    'region_injuries': {
                        'region': row['BEAT_OF_OCCURRENCE'],
                        'injuries_total': 1 if injuries_total == 0 else injuries_total
                    }
                }
            },
            upsert=True
        )

        month = row['CRASH_DATE'][0:2]

        monthly_injuries.update_one(
            {'month': month, 'region_injuries.region': row['BEAT_OF_OCCURRENCE']},
            {
                '$inc': {
                    'region_injuries.$.injuries_total': injuries_total
                }
            }
        )

        monthly_injuries.update_one(
            {'month': month},
            {
                '$addToSet': {
                    'region_injuries': {
                        'region': row['BEAT_OF_OCCURRENCE'],
                        'injuries_total': 1 if injuries_total == 0 else injuries_total
                    }
                }
            },
            upsert=True
        )


def add_indexes():
    region_injuries.create_index([('region', 1)])

    region_cause_of_death.create_index([('region', 1)])

    daily_injuries.create_index([('date', 1)])
    daily_injuries.create_index([('date', 1), ('region_injuries.region', 1)])

    monthly_injuries.create_index([('month', 1)])
    monthly_injuries.create_index([('month', 1), ('region_injuries.region', 1)])




if __name__ == '__main__':
    init_crash_db('../assets/data.csv')
    add_indexes()
    pass
