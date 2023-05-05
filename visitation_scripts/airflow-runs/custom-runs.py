import requests
import json
import datetime as dt
import time
import logging
import logging.config
import os

file_path = dir_path = os.path.dirname(os.path.realpath(__file__))
print(file_path)

logging.config.fileConfig(file_path+'/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger("spark-runs")

class AirflowDagRuns():

    __logger__ = logging.getLogger("spark-runs")
    __cookie__ = "session=26a81126-bdda-4dad-8705-9022b23ecdae.q3rnK8Gtk2TSxrfqEn2IoDzekxQ; Expires=Fri, 03 Mar 2023 08:25:14 GMT; HttpOnly; Path=/; SameSite=Lax"
    __content_type__ = 'application/json'
        
    def __init__(self, dag_id:str) -> None:
        self.__dag_id__:str = dag_id#"visitation_step_0"#"mobility_preprocess"#
        self.__dag_run_id__:str = ""
        self.__count__:int = 30
        self.__completed__:bool = False

    def __run_dags__(self,dag_id, dag_run_id,input_date, country):
        
        res = {}
        try:
            url = f"http://129.80.94.208:8080/api/v1/dags/{dag_id}/dagRuns"
            
            if dag_id.isin(["visitation_step_0","visitation_step_1","visitation_step_4"]):
                payload = json.dumps({
                "dag_run_id": dag_run_id,
                "conf": {
                    "input_date": input_date,
                    "country": country
                }
                })
            elif dag_id.isin(["visitation_step_2"]):
                payload = json.dumps({
                "dag_run_id": dag_run_id,
                "conf": {
                    "input_date": input_date,
                    "country": country,
                    "version": " "
                }
                })

            headers = {
              'Content-Type': self.__content_type__,
              'Accept': self.__content_type__,
              'Cookie': self.__cookie__
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            res = response.json()
            print("res",res)
            if "status" in res:
                if res["status"]  == 409:
                    print("Throw exception")
                    logger.error(res)
                    raise Exception("Data already exist")

            self.__logger__.info(f"message='Dag run started for {dag_run_id}';dag_response={res};dag_run_id={dag_run_id}")
            return res
        except Exception as e:
            self.__logger__.error(e)
            if res["status"] == 409:
                self.__count__ = self.__count__ + 100
                self.execute(dag_id=dag_id, dag_run_id=dag_run_id, input_date=input_date, country=country)


    def __check_status__(self,dag_id, dag_run_id):
        url = f"http://129.80.94.208:8080/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}"

        payload={}
        headers = {
        'Content-Type': self.__content_type__,
        'Accept': self.__content_type__,
        'Cookie': self.__cookie__
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.json()
        self.__logger__.info(f"message='Check Status for {dag_run_id}';dag_res={res}; dag_run_id={dag_run_id}")

        if(res["state"] == "failed"):
            self.__logger__.error(f"message='Job failed for {dag_run_id}';dag_res={res}; dag_run_id={dag_run_id}")
            raise Exception("Job failed")

        return res


    def execute(self, dag_id, dag_run_id, input_date, country):
        self.__count__
        try:
            dag_run_id_ = dag_run_id+str(self.__count__)
            self.__logger__.info(f"message='Initiate job for {dag_run_id}';dag_run_id={dag_run_id}")
            res = self.__run_dags__(dag_id=dag_id, dag_run_id=dag_run_id_, input_date=input_date, country=country)
            global completed 

            # check dag runs
            check = 0
            time.sleep(120)
            while completed == False:
                res = self.__check_status__(dag_id=dag_id, dag_run_id= dag_run_id_)
                check += 1
                self.__logger__.info(f"message='Check started for {dag_run_id_}, checked_count={check}'; dag_run_id={dag_run_id}")
                if res["state"] == 'success':
                    self.__logger__.info("completed")
                    completed = True
                time.sleep(60)

        except Exception as e:
            self.__logger__.error(e)
            self.__count__ += 1

start_date = "2023-01-02"
end_date = "2023-01-06"
start_date_value = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
start_date_day = (dt.datetime.now().date() - start_date_value).days
 
#get no of days from today till end date.
end_date_value = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
end_date_day = (dt.datetime.now().date() - end_date_value).days

#create a list of number of days from start till end 
number_of_days = [x for x in range(end_date_day,start_date_day+1)]
number_of_days.sort(reverse=True)

#day_values =[ (datetime.datetime.now()-datetime.timedelta(days = x)).strftime("%Y-%m-%d") for x in number_of_days]
day_values =[ (dt.datetime.now()-dt.timedelta(days = x)).strftime("%Y-%m-%d") for x in number_of_days]

date_list = day_values

all_dag_id = ["visitation_step_0", "visitation_step_1", "visitation_step_2", "visitation_step_3", "visitation_step_4", "visitation_step_5"]
#dag_id = all_dag_id[2]#"visitation_step_1"
logger.info(f"dag_run='{dag_id}';message='All date list {date_list}'")      #### doubt
country = "'IND'"
#ar_runs = AirflowDagRuns(dag_id=dag_id)


for day in date_list:
    input_date = f"'{day}'"
    for id in all_dag_id:
        dag_id = id
        ar_runs = AirflowDagRuns(dag_id=dag_id)
        dag_run_id = f"{dag_id}-{str(input_date)}-{country}-".replace("'","")
        completed = False
        ar_runs.execute(dag_id=dag_id, dag_run_id=dag_run_id, input_date=input_date, country=country)
        if completed == True:
            logger.info(f"message='completed job for {dag_run_id}';dag_run_id={dag_run_id}")
            time.sleep(60)
