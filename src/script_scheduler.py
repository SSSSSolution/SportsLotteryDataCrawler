import time
import datetime
import schedule
import logging
import subprocess
import json
from get_data import get_data

def job():
    try:
        now = datetime.datetime.now().time()
        weekday_start_time = datetime.datetime.strptime(config['weekday']['start_time'], "%H:%M").time()
        weekday_end_time = datetime.datetime.strptime(config['weekday']['end_time'], "%H:%M").time()
        weekend_start_time = datetime.datetime.strptime(config['weekend']['start_time'], "%H:%M").time()
        weekend_end_time = datetime.datetime.strptime(config['weekend']['end_time'], "%H:%M").time()

        if schedule.datetime.datetime.today().weekday() < 5:
            if weekday_start_time <= now <= weekday_end_time:
                get_data()
        else:
            if weekend_start_time <= now <= weekend_end_time:
                get_data()
    except Exception as e:
        logging.error("Get data failed: " + str(e))



with open('..\\config.json') as f:
    config = json.load(f)

# set logger
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('PIL').setLevel(logging.INFO)
logging.getLogger('matplotlib.font_manager').setLevel(logging.INFO)

interval_minutes = config['interval_minutes']

schedule.every(interval_minutes).minutes.do(job)

job()
while True:
    schedule.run_pending()
    time.sleep(60)