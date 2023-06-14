import time
import json
from src.sporttery_data_getter import SportteryDataGetter

s = SportteryDataGetter()

sporttery_datas = {}

max_retries = 3

try:
    for attempt in range(max_retries):
        try:
            sporttery_datas = s.get_data()
            break
        except Exception as e:
            print(f"Exception caught: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
                time.sleep(30)
            else:
                raise
except Exception as e:
    print("Failed to get sporttery datas: ", e);

print(json.dumps(sporttery_datas, ensure_ascii=False, indent=4))

try:
    with open('tmp/sporttery_datas.json', 'w') as file:
        json.dump(sporttery_datas, file, ensure_ascii=False, indent=4)
    print("JSON data saved successfully.")
except Exception as e:
    print(f"Error occurred while saving JSON data: {e}")