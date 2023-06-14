import json
from src.excel_writer import ExcelWriter

try:
    with open('tmp/sporttery_datas.json', 'r') as f:
        sporttery_datas = json.load(f)

    with open('tmp/okooo_datas.json', 'r') as f:
        okooo_datas = json.load(f)
except Exception as e:
    print(f"Error occurred while reading JSON data: {e}")

writer = ExcelWriter()
writer.write_datas(sporttery_datas, okooo_datas)