import csv
import yaml
import sqlite3


cur = ''
with open("aims/config.yaml", 'r') as yaml_file:
    cfg = yaml.safe_load(yaml_file)
    db_path = cfg['mysql']['db']
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

query = "select time_of_accident as date, count(accident_id)as num_of_accidents " \
        " from final_accident_report group by strftime('%m ',time_of_accident)  "
cursor = cur.execute(query)

with open("CSVs/accidents_in_month.csv", "w+") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

query = "select accident as accident_type, sum(victims)as casualty  from final_accident_report as af inner join" \
        " accident as a on a.id=af.accident_id inner join accident_type as at on at.id=a.type group by (accident) "
cursor = cur.execute(query)

with open("CSVs/casualty_rate.csv", "w+") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

