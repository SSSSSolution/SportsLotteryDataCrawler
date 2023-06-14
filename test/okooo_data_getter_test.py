import time
import json
from src.okooo_data_getter import OkoooDataGetter

g = OkoooDataGetter()
okooo_datas = {}

max_retries = 3
try:
    for attempt in range(max_retries):
        try:
            okooo_datas = g.get_data()
            break
        except Exception as e:
            print(f"Exception caught: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
                time.sleep(30)
            else:
                raise
except Exception as e:
    print("Failed to get okooo datas: ", e);

print(json.dumps(okooo_datas, ensure_ascii=False, indent=4))

try:
    with open('tmp/okooo_datas.json', 'w') as file:
        json.dump(okooo_datas, file, ensure_ascii=False, indent=4)
    print("JSON data saved successfully.")
except Exception as e:
    print(f"Error occurred while saving JSON data: {e}")