import time
import logging
from okooo_data_getter import OkoooDataGetter
from sporttery_data_getter import SportteryDataGetter
from excel_writer import ExcelWriter


def get_data():
    logging.info("get data")
    max_retries = 3
    try:
        sporttery_data_getter = SportteryDataGetter()
        for attempt in range(max_retries):
            try:
                sporttery_datas = sporttery_data_getter.get_data()
                break
            except Exception as e:
                logging.error(f"Exception caught: {e}")
                if attempt < max_retries - 1:
                    logging.info("Retrying to get sporttery datas...")
                    time.sleep(30)
                else:
                    raise
    except Exception as e:
        logging.error("Failed to get sporttery datas: ", e)
        raise

    try:
        okooo_data_getter = OkoooDataGetter()
        for attempt in range(max_retries):
            try:
                okooo_data_datas = okooo_data_getter.get_data()
                break
            except Exception as e:
                logging.error(f"Exception caught: {e}")
                if attempt < max_retries - 1:
                    logging.info("Retrying to get okooo datas...")
                    time.sleep(30)
                else:
                    raise
    except Exception as e:
        logging.error("Failed to get okooo datas: ", e)
        raise
    #print(okooo_data_getter.session.cookies)

    try:
        excel_writer = ExcelWriter()
        excel_writer.write_datas(sporttery_datas, okooo_data_datas)
    except Exception as e:
        logging.error("Failed to write excel file: ", e)
        raise










