from database.connect import region_injuries, region_cause_of_death, daily_injuries, monthly_injuries
from services.csv_service import read_csv


def init_crash_db():
    region_injuries.drop()
    region_cause_of_death.drop()
    daily_injuries.drop()
    monthly_injuries.drop()

    for row in read_csv('../assets/data.csv'):
        injuries_total = int(row['INJURIES_TOTAL']) if row['INJURIES_TOTAL'].strip() else 0
        fatal_injuries = int(row['INJURIES_FATAL'].strip()) if row['INJURIES_FATAL'].strip() else 0
        non_fatal_injuries = int(row['INJURIES_NON_INCAPACITATING'].strip()) if row[
            'INJURIES_NON_INCAPACITATING'].strip() else 0

        injuries_data = {
            'injuries_total': injuries_total,
            'fatal_injuries': fatal_injuries,
            'non_fatal_injuries': non_fatal_injuries,
            'injuries_list': [
                row['MOST_SEVERE_INJURY']
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
                '$push': {
                    'injuries_list': row['MOST_SEVERE_INJURY']
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
            {'date': row['CRASH_DATE'], 'region_injuries.region': row['BEAT_OF_OCCURRENCE']},
            {
                '$inc': {
                    'region_injuries.$.injuries_total': injuries_data['injuries_total']
                }
            }
        )

        daily_injuries.update_one(
            {'date': row['CRASH_DATE']},
            {
                '$addToSet': {
                    'region_injuries': {
                        'region': row['BEAT_OF_OCCURRENCE'],
                        'injuries_total': injuries_data['injuries_total']
                    }
                }
            },
            upsert=True
        )

        month = row['CRASH_DATE'][3:5]
        injuries_data = {
            'injuries_total': int(row['INJURIES_TOTAL']) if row['INJURIES_TOTAL'].strip() else 0
        }

        monthly_injuries.update_one(
            {'month': month, 'region_injuries.region': row['BEAT_OF_OCCURRENCE']},
            {
                '$inc': {
                    'region_injuries.$.injuries_total': injuries_data['injuries_total']
                }
            }
        )

        monthly_injuries.update_one(
            {'month': month},
            {
                '$addToSet': {
                    'region_injuries': {
                        'region': row['BEAT_OF_OCCURRENCE'],
                        'injuries_total': injuries_data['injuries_total']
                    }
                }
            },
            upsert=True
        )

    region_injuries.create_index([('region', 1)])

    region_cause_of_death.create_index([('region', 1)])

    daily_injuries.create_index([('date', 1)])
    daily_injuries.create_index([('date', 1), ('region_injuries.region', 1)])

    monthly_injuries.create_index([('month', 1)])
    monthly_injuries.create_index([('month', 1), ('region_injuries.region', 1)])


if __name__ == '__main__':
    init_crash_db()
