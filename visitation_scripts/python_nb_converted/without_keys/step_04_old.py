# %%
print("starting...")



# -*- coding: utf-8 -*-
"""part_1_mobility_script_generic(new_dataset)_new (2).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dGNHBaJAS1w2hsZw4c_Kx4bFdQ0Kzdg_
"""

print("starting...")

from pyspark.sql.window import Window 
import pyspark
from pyspark import SparkContext

from pyspark.sql import functions as F
import pyspark.sql.functions as func


from pyspark.sql.functions import udf
from pyspark.sql.types import *
from pyspark.sql.functions import col, window
import pyspark.sql.functions as func
from pyspark.sql.functions import desc
import datetime, time
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.window import Window
import pyspark.sql.functions as sf

import datetime as dt
import numpy as np
import os

from multiprocessing.pool import Pool
import pickle
import pandas as pd

from h3 import h3


from math import radians, cos, sin, asin, sqrt
from pyspark.sql.functions import lit
import json

from datetime import datetime, date, timedelta

#spark.conf.set("fs.azure.account.key.iasocialdata.dfs.core.windows.net",
#"5NXk2QYSRf4tbGSG1Sx20Seg6lkABbERa7ao2h0ZxWbSkLQtuy3+9yYDgr6+FDRKy1Rloi0d2dWa2XmF657SwQ==")
#spark.conf.set("spark.sql.execution.arrow.enabled", "true")  #### Enable Arrow-based columnar data transfers

#sc.install_pypi_package("boto3==1.16.35")
#sc.install_pypi_package("SqlAlchemy")
#sc.install_pypi_package("pymysql")

# from pyspark.sql import SparkSession
# spark = SparkSession.builder.appName("S3CSVRead").getOrCreate()

#accessKeyId =  dbutils.secrets.get(scope = "old-aws-account", key = "privateKey")
#secretAccessKey = dbutils.secrets.get(scope = "old-aws-account", key = "secretAccessKey")


from pyspark.sql import SparkSession
import sys
import boto3
from io import BytesIO

from functools import reduce
from pyspark.sql import DataFrame

from pyspark.sql.functions import round, col
from dateutil import tz
import sqlalchemy as db

## oci imports
import oci
import os
import io
import sys
from pathlib import Path
from oci.config import validate_config
from oci.object_storage import ObjectStorageClient

#ociconf = oci.config.from_file()

spark = SparkSession.builder.appName("step_04") \
        .config("spark.default.parallelism", '120')\
        .config("spark.scheduler.mode", "FAIR") \
        .config("spark.pyspark.virtualenv.enabled", "true") \
        .config("spark.delta.logStore.oci.impl","io.delta.storage.OracleCloudLogStore")\
        .config("fs.oci.client.custom.authenticator", "com.oracle.bmc.hdfs.auth.InstancePrincipalsCustomAuthenticator")\
        .config('fs.oci.client.hostname', "https://objectstorage.us-ashburn-1.oraclecloud.com")\
        .config('fs.oci.client.auth.tenantId.region', "us-ashburn-1")\
        .getOrCreate()
#        .config("spark.dynamicAllocation.enabled", "true") \
#        .config("spark.shuffle.service.enabled", "true")\
#        .config("spark.network.timeout","300")\
        
#        .config("spark.cores.max", "190") \
#spark.conf.set('fs.oci.client.auth.tenantId', "ocid1.tenancy.oc1..aaaaaaaamqxmfclvmrazpk4kt7ibkcfzfg2fvg4o2wyzemzu3n7tcpf6nvsa")
#spark.conf.set('fs.oci.client.auth.userId', "ocid1.user.oc1..aaaaaaaa4gjumyz4kiowhzbyjzgajyo5bln565rntgboqod3t6lu4bpwl2ra")
#spark.conf.set('fs.oci.client.auth.fingerprint', "ec:8f:0e:14:e0:31:cd:e4:d6:03:04:aa:aa:94:f9:a9")
#spark.conf.set('fs.oci.client.auth.pemfilepath', "~/.oci/oci_api_key")
#spark.conf.set('fs.oci.client.auth.tenantId.region', "us-ashburn-1")
#spark.conf.set('fs.oci.client.hostname', "https://objectstorage.us-ashburn-1.oraclecloud.com")

print(spark.sparkContext._conf.getAll())
#print(ociconf)
print(spark.sparkContext.defaultParallelism)


spark.conf.set("spark.hadoop.fs.s3a.multipart.size", "114857600")

# %%
### Arguments 

client= "all_ind_all_poi_v3.1.6"#dbutils.widgets.get('client')#"Test_silver_level"
input_date= "2022-07-07"#dbutils.widgets.get('input_date')#"2021-08-11"
version = ""
indexing_level=12#int(dbutils.widgets.get('indexing_level'))#int("12")
time_spent_at_target_location_2= 0#int(dbutils.widgets.get('starting_limit'))#"0"
time_spent_at_target_location_2_upper_limit= 120#int(dbutils.widgets.get('ending_limit'))#"120"
starting_limit_hour= 7#int(dbutils.widgets.get('starting_limit_hour')) #int("7")
ending_limit_hour= 200#int(dbutils.widgets.get('ending_limit_hour')) #int("20")
country= "IND"#dbutils.widgets.get('country') #"IND"
poi_type = ""#dbutils.widgets.get('poi_type')#"POI.UAE.restaurants, POI.Shopping.Supermarket, POI.Public.School.UAE"#
district_code = ""#dbutils.widgets.get('district_code') #"IN.MH.MC"
source = "GRAVY"#dbutils.widgets.get('source') 

''''client= "test_grvay_pfizer"
input_date= "2022-05-17"

indexing_level=int("12")
time_spent_at_target_location_2= int("0")
time_spent_at_target_location_2_upper_limit= int("120")
starting_limit_hour= int("7")
ending_limit_hour= int("20")
country= "IND"
poi_type = "health.clinic, health.clinic.dentist, health.clinic.health_centre, health.clinic.physician, health.service.pharmacy, health.service.drugstore,health.hospital, health.hospital.general, health.hospital.emergency_room, health.hospital.nursing_home"
district_code ="IN.KA.BN,IN.KA.BR,IN.MH.MC,IN.MH.MU,IN.DL.CD,IN.DL.ED,IN.DL.ND,IN.DL.NO,IN.DL.NE,IN.DL.NW,IN.DL.SH,IN.DL.SD,IN.DL.SED,IN.DL.SW,IN.DL.WD"
source = "gravy"'''

today = (date.today()).strftime("yyyy-mm-dd")


### POI data (sample)
##save_string = "s3://ia-customer-insights/poitype_list/USA/US-Burger-King/107ff9cb2caafbefdda5ab1d906fc42a46f749ad.csv.gz/"

str_arg = ""

if(starting_limit_hour == ""):
    starting_limit_hour = 7

if(ending_limit_hour == ""):
    ending_limit_hour = 203

# %%
poi_type_list = poi_type.split(',')
hash_poi = ",".join(sorted(poi_type_list)) + str(indexing_level)
import hashlib
# hash_poi = str(abs(hash(hash_poi)) % (10 ** 8))
unique_t =f"poi-{str(indexing_level)}-{country}-{client}" 
poi_string = ",".join(sorted(poi_type_list)) + unique_t
hash_poi = str(hashlib.sha1(poi_string.encode('utf-8')).hexdigest())

district_code_list = []
if(district_code != ''):
    district_code_list = district_code.split(',')
    

# %%
start_date = "2022-07-08"
end_date = "2022-08-10"

#get no of days from today till start date
start_date_value = datetime.strptime(start_date, "%Y-%m-%d").date()
start_date_day = (datetime.now().date() - start_date_value).days

#get no of days from today till end date.
end_date_value = datetime.strptime(end_date, "%Y-%m-%d").date()
end_date_day = (datetime.now().date() - end_date_value).days

#create a list of number of days from start till end 
number_of_days = [x for x in range(end_date_day,start_date_day+1)]
number_of_days.sort(reverse=True)

day_values =[ (datetime.now()-timedelta(days = x)).strftime("%Y-%m-%d") for x in number_of_days]

namespace = "bmmp5bv7olp2"

signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
identity_client = oci.identity.IdentityClient(config={}, signer=signer)
today = datetime.today().strftime('%Y-%m-%d')
    
for input_date in day_values:
    token = f"test_poi_pipeline_{country}_{input_date}_{client}_{source}"
    print(f"Staretd for date={input_date}")

    def createLogs():
        try:
            f = BytesIO()

            bucket_name = "ia-mobility-logs"
            more_binary_data = str(f.getvalue().decode()) + "request_id="+token+";notebook_name=Gold table processing;start_time="+str(time.time())+"\n request_id="+token+";message=Gold Silver table processing \n"
            #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
            # Method 1: Object.put()

            logs_path = f"logs/{client}/{hash_poi}/{today}_{input_date}_new_mobility_step_04.txt"
            object_storage_client = ObjectStorageClient(signer=signer, config={})
        
            object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
        except Exception as e:
            print(e)

    createLogs()

    def writeToLogs(str_arg):
        try:
            f = BytesIO()
            bucket_name = "ia-mobility-logs"
            logs_path = f"logs/{client}/{hash_poi}/{today}_{input_date}_new_mobility_step_04.txt"
            object_storage_client = ObjectStorageClient(signer=signer, config={})
            file_data = object_storage_client.get_object(namespace,bucket_name, logs_path)
        
            more_binary_data = str(file_data.data.text)+"\n"+"notebook_name=Gold table processing;" + str(str_arg)
            #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
            # Method 1: Object.put()
            object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
            return "completed"
        
        except Exception as e:
            print(e)
            return e

    start_time = time.time()
    save_string = f"oci://ia-visitation-data@bmmp5bv7olp2/poitype_list/delta/step_03_alt/{str(hash_poi)}/"
    #f"s3://ia-customer-insights/poitype_list/delta/temp_pois/{str(hash_poi)}/{client}/"
    if(district_code != ''):
        df_poi = spark.read.format("delta").load(save_string.split(','),header = True)\
        .where((col('country') == country)& (col('district_code').isin(district_code_list))) #col("version") == version) &
    else: 
        df_poi = spark.read.format("delta").load(save_string.split(','),header = True)\
        .filter((col('country') == country))
        #col("version") == version) &
    #df_poi = df_poi.filter()
    #df_poi.show(2)  
    print("in try POI ....")
    print(save_string)
    log_str= "request_id="+token+";task_id=1.1;task_name=Read file from Existing hash of POI;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)
    
    ### Daily user data (sample)
    ##save_string = "s3://ia-customer-insights/silver_level_test/"+country+"/daily_data/"+input_date+".csv.gz"
    start_time = time.time()
    #if source =="gravy":
    #    country="IN"
    #    save_string = "oci://ia-datapipeline@bmmp5bv7olp2/mobility_vendor_eval/gravy_may/IN/copper_layers_all/date="+input_date
    #else:
    save_string = f"oci://ia-visitation-data@bmmp5bv7olp2/silver_level_first/daily_data/delta/step_2/{source.lower()}/"
    # save_string = "s3://ia-customer-insights/silver_level_first/{0}/daily_data/delta/{1}".format(country, input_date)
    print(save_string)

    if(district_code != ''):
        ifa_indexed_store = spark.read.format("delta")\
                    .load(save_string.split(','),header = True)\
                    .where((col('country') == country) & (col('date') == input_date) &
                    (col('district_code').isin(district_code_list)))
    else: 
        ifa_indexed_store = spark.read.format("delta")\
                    .load(save_string.split(','),header = True)\
                    .where((col('country') == country) & (col('date') == input_date)) #& (col("version") == version))
    #ifa_indexed_store = ifa_indexed_store.filter(col('district_code').isin(district_code_list))

    log_str= "request_id="+token+";task_id=2.0;task_name=Read silver;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    print(writeToLogs(log_str))
    #ifa_indexed_store.show(2)
    print(ifa_indexed_store.count())
    
    '''
    if(district_code != ""):
    start_time = time.time()
    ifa_indexed_store = ifa_indexed_store.filter(ifa_indexed_store.city.isin(district_code_list))
    print(ifa_indexed_store.count())
    log_str= "request_id="+token+";task_id=2.1.1;task_name=Filter diistrict code;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    print(writeToLogs(log_str))

    '''

    if(poi_type != ''):
        start_time = time.time()
        df_poi_1 = df_poi.filter(df_poi.poiType.isin(poi_type_list))
        #df_poi_1.show(3)
        log_str= "request_id="+token+";task_id=2.1.2;task_name=Filter poiType;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
        print(writeToLogs(log_str))
        print(df_poi_1.count())
    else: 
        df_poi_1 = df_poi

    if(poi_type == "" and district_code == ""):
        data_union = ifa_indexed_store.join(df_poi_1, how="inner",on=["h12_int"])\
            .select(df_poi_1.version,ifa_indexed_store.h12 , ifa_indexed_store.h6,ifa_indexed_store.h12_int, ifa_indexed_store.h6_int, ifa_indexed_store.ifa, ifa_indexed_store.date,          ifa_indexed_store.timestamp, ifa_indexed_store.country, ifa_indexed_store.district_code, 
                    df_poi_1.poiCode, df_poi_1.poiType, df_poi_1.h3, df_poi_1.time_spent_at_target_location_2,
                   df_poi_1.time_spent_at_target_location_2_upper_limit, df_poi_1.starting_limit_hour, df_poi_1.ending_limit_hour
                   )
    else:
        data_union = ifa_indexed_store.join(broadcast(df_poi_1), ifa_indexed_store.h12_int == df_poi_1.h12_int)\
            .select(df_poi_1.version,ifa_indexed_store.h12 , ifa_indexed_store.h6,ifa_indexed_store.h12_int, ifa_indexed_store.h6_int, ifa_indexed_store.ifa, ifa_indexed_store.date,          ifa_indexed_store.timestamp, ifa_indexed_store.country, ifa_indexed_store.district_code, 
                    df_poi_1.poiCode, df_poi_1.poiType, df_poi_1.h3, df_poi_1.time_spent_at_target_location_2,
                   df_poi_1.time_spent_at_target_location_2_upper_limit, df_poi_1.starting_limit_hour, df_poi_1.ending_limit_hour
                   )
    

    #data_union.show(3)
    
    start_time = time.time()
    ##### hour of the day
    from pyspark.sql.functions import substring
    #substring(str, pos, len)
    data_union = data_union.withColumn("hour_of_day", substring(col("timestamp"),12,2))

    #data_union.show(3)
    print(data_union.count())
    log_str= "request_id="+token+";task_id=2.2;task_name=Add hour of day;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    print(writeToLogs(log_str))
    
    #BEFORE
    #dfm_join = ifa_indexed_store.selectExpr("h12", "h6", "lat", "long", "ifa", "date","timestamp","city","poiCode", "poiType as poiTypeId", "hour_of_day")
    #AFTER
    dfm_join = data_union.selectExpr("version","h12", "h6", "h3", "ifa", "date","timestamp","district_code as city","poiCode", "poiType as poiTypeId", "hour_of_day", "ending_limit_hour", "starting_limit_hour", "time_spent_at_target_location_2", "time_spent_at_target_location_2_upper_limit", )


    #.join(df_poi, on=["h6","h12"], how='inner').select(ifa_indexed_store.h12, ifa_indexed_store.h6,ifa_indexed_store.lat, ifa_indexed_store.long, ifa_indexed_store.ifa, ifa_indexed_store.date,ifa_indexed_store.timestamp, ifa_indexed_store.city, df_poi.poiCode, df_poi.poiTypeId, ifa_indexed_store.hour_of_day).orderBy(['h6', 'h12'],ascending=True)


    #dfm_join_filtered = dfm_join.filter(dfm_join.h6 == "8643a136fffffff")

    #dfm_join.show(3)
    
    ### Joining on common h12

    from pyspark.sql.types import IntegerType




    #dfm = dfm.select(dfm.h12, dfm.h6, dfm.h3, dfm.ifa, dfm.lat, dfm.long, dfm.date, dfm.timestamp, dfm.city, dfm.hour_of_day)

    #dfm_join.show(3)
    start_time = time.time()
    dfm_join = dfm_join.withColumn("hour_of_day", dfm_join["hour_of_day"].cast(IntegerType())) \
                   .withColumn("starting_limit_hour", dfm_join["starting_limit_hour"].cast(IntegerType())) \
                   .withColumn("ending_limit_hour", dfm_join["ending_limit_hour"].cast(IntegerType()))

    dfm = dfm_join.filter((dfm_join.hour_of_day > dfm_join.starting_limit_hour) & (dfm_join.hour_of_day < dfm_join.ending_limit_hour))

    log_str= "request_id="+token+";task_id=2.5;task_name=Filter on opening and closing time;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    print(writeToLogs(log_str))

    dfm.show(3)

    paths = "oci://ia-visitation-data@bmmp5bv7olp2/intermediate_date/generic_joined1/step_04/"+token
    dfm.write.format("parquet").mode('overwrite').option("timestampFormat", "yyyy-MM-dd HH:mm:ss").save(paths ,header =True)
    paths = "oci://ia-visitation-data@bmmp5bv7olp2/intermediate_date/generic_joined1/step_04/"+token
    print(paths)
    df = spark.read.format("parquet").load(paths.split(','),header = True)
    # df_func_done = df.selectExpr('h3 as h3_orig', 'ifa as ifa', 'lat as lat', 'long as long', 'date as date', 'carrier as carrier', 'zipcode as zipcode', 'city as city', 'timestamp as timestamp')
    # df_func_done.show(3)
    if source == "gravy":
        df = df.withColumn("date", substring(col("timestamp"),0,10))

    #df.show(3)

    start_time = time.time()
    ### UDF(user defined function) to calculate time delta
    def calculate_distance(time_prev, time_next):
      if(type(time_prev) == str and type(time_next) == str):
        time1 = dt.datetime.strptime(time_prev, '%Y-%m-%d %H:%M:%S')
        time2 = dt.datetime.strptime(time_next, '%Y-%m-%d %H:%M:%S')
        time_delta = (time2 - time1).total_seconds()/60
      else:
        time_delta = (time_next - time_prev).total_seconds()/60
    
        return [str(time_delta)]

    schema = StructType([
        StructField("time", StringType(), False)
    ])

    loc_test2 = udf(lambda a,b: calculate_distance(a,b), schema)


    #df.count()
    df  = df.withColumn("timestamp", F.to_timestamp("timestamp"))
    #df.show(3)
    ### User-level filtering and aggregations

    sample_with_lag = df.withColumn('timestamp_lag', func.lag(df['timestamp']).over(Window.partitionBy(["ifa","date"]).orderBy(func.col("timestamp").asc())))
    sample_with_lag = sample_with_lag.withColumn('poiCode_lag', func.lag(sample_with_lag['h12']).over(Window.partitionBy(["ifa","date"]).orderBy(func.col("timestamp").asc())))
    sample_with_lag = sample_with_lag.orderBy("timestamp")
    #sample_with_lag.show(3)

    sample_with_lag = sample_with_lag.filter(sample_with_lag.timestamp_lag.isNotNull())
    #sample_with_lag.show(3)
    #print(sample_with_lag.columns)

    ### Added ,'h3', 'lat', 'long' to sample_with_lag on date 2022-05-23
    sample_with_lag = sample_with_lag.select('version','h6','h12','h3','ifa', 'timestamp', 'city', 'hour_of_day', 'poiCode', 'poiTypeId', 'date', 'timestamp_lag', 'poiCode_lag','time_spent_at_target_location_2',
                                        'time_spent_at_target_location_2_upper_limit' ,loc_test2('timestamp_lag','timestamp').alias('tdelta'))
    sample_with_lag = sample_with_lag.select('version','h6','h12','h3', 'ifa', 'timestamp', 'city', 'hour_of_day', 'poiCode', 'poiTypeId', 'date', 'timestamp_lag', 'poiCode_lag',
                                         "time_spent_at_target_location_2","time_spent_at_target_location_2_upper_limit","tdelta.time")
    #sample_with_lag.show(3)

    #x  = sample_with_lag.select('ifa').distinct().count()

    #print(x)
    sample_with_lag2 = sample_with_lag.groupBy(["version","ifa","date","h12", "time_spent_at_target_location_2", "time_spent_at_target_location_2_upper_limit"])\
                                 .agg(F.sum("time").alias("all_time"))
    #sample_with_lag2.show(3)

    log_str= "request_id="+token+";task_id=2.6;task_name=Filter on time spent on pois;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)
    
    
    # remove # in the line below after this test 
    visitor = sample_with_lag2#.filter((sample_with_lag2.all_time > sample_with_lag2.time_spent_at_target_location_2) & (sample_with_lag2.all_time < sample_with_lag2.time_spent_at_target_location_2_upper_limit)).select('ifa').distinct()

    #y= visitor.count()
    #print(y)

    # uncomment following line and the part before ".join"
    #before
    #dist = visitor.select('ifa').distinct()
    #dfx1 = df.join(dist, on=["ifa"], how='inner')
    #dfx1.show(3)

    #after
    dist = visitor.dropDuplicates(subset = ['ifa'])
    dist1 = dist.select('ifa','all_time')
    dfx1 = df.join(dist1, on=["ifa"], how='inner')
    #dfx1.show(3)

    dfx1 = dfx1.selectExpr("ifa","date","poiCode","poiTypeId","all_time as visit_duration", "version")
    dfx1 = dfx1.dropDuplicates()

    from pyspark.sql.functions import substring
    dfx1 = dfx1.withColumn("month", dfx1.date.substr(6,2))

    from pyspark.sql.functions import lit
    dfx1 = dfx1.withColumn("customer", lit(client))

    dfx1 = dfx1.dropDuplicates()

    dfx2 = dfx1.withColumn("source", lit(source))


    # dfx1.show(3)

    # dfx1.write.format("csv").mode('overwrite').option("timestampFormat", "yyyy-MM-dd HH:mm:ss").save("s3://ia-customer-insights/pfizer/lists_update/list_"+token+".csv.gz" ,header =True)
    # save_string = "s3://ia-customer-insights/pfizer/lists_update_3/vaccination_centers/list_"+token+".csv.gz"
    # print(save_string)
    start_time = time.time()
    #if source =="ls":
    save_string = f"oci://ia-visitation-data@bmmp5bv7olp2/poiVisit/delta/{country}/" +"all_ind_all_poi_incremented"+"/"+str(indexing_level)+"/"
    #else:
    #    save_string = "oci://ia-datapipeline@bmmp5bv7olp2/mobility_vendor_eval/gravy_may/IN/gold_ouput/" +client+"/"+str(indexing_level)+"/"+token
    print(save_string)
    #update to overwrite from append
    dfx2.write.partitionBy(["version","source","month","date"]).format("delta")\
    .option("overwriteschema", "true")\
    .mode('append').option("timestampFormat", "yyyy-MM-dd HH:mm:ss").save(save_string,header =True)
    #dfx2.show(3)
    log_str= "request_id="+token+";task_id=3.0;task_name=Write file to delta;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok"
    print(writeToLogs(log_str))
    
    print(f"Completed for date ={input_date}")


    

# %%


# %%


# %%
#create SQL table 
#spark.sql("Drop TABLE df_poi_delta")
#spark.sql("CREATE TABLE df_poi_delta USING DELTA LOCATION 's3://ia-customer-insights/poitype_list/delta/IND/TEST_MH_ALL/7b52009b64fd0a2a49e6d8a939753077792b0554'")
#spark.catalog.listTables()
#spark.sql("select * from df_poi_delta").show(3)

# %%
##OPTIMIZE df_poi ZORDER BY (h6, h12)
#spark.sql("OPTIMIZE df_poi_delta ZORDER BY (poiType,h12)")
#df_poi = spark.sql("select poiCode as poiCode, poiType as poiTypeId, h12, h6,h3,p_city as city  from df_poi_delta")
#df_poi = df_poi.filter(df_poi.city.isin(district_code_list))
#df_poi.show(3)

# %%


# %%


# %%


# %%


# %%
#ifa_indexed_store = spark.read.format("delta").load(save_string.split(','),header = True)
#dp_poicode_unique = ifa_indexed_store.groupBy('poiCode').count().orderBy('count', ascending=False)

#display(dp_poicode_unique)

# %%


# %%
'''
start_time = time.time()
paths = "s3://ia-customer-insights/intermediate_date/generic_joined1_join_"+token
dfm_join.write.partitionBy(['h6','poiTypeId', "hour_of_day"]).format("parquet").mode('overwrite').option("timestampFormat", "yyyy-MM-dd HH:mm:ss").save(paths ,header =True)
log_str= "request_id="+token+";task_id=2.3;task_name=write join file;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok"
print(writeToLogs(log_str))
'''
dfm_join.printSchema()

# %%
'''
#paths = "s3://ia-customer-insights/intermediate_date/generic_joined1_join"+token+"/*.parquet"
start_time = time.time()
paths = "s3://ia-customer-insights/intermediate_date/generic_joined1_join_"+token
dfm_join = spark.read.format("parquet").load(paths, header = 'true')
log_str= "request_id="+token+";task_id=2.4;task_name=Read intermediate file;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
print(writeToLogs(log_str))
dfm_join.show(3)

print(dfm_join.count())
'''

# %%
#dfm_join.groupby("ifa").count().show()

#dfm_join.distinct().count()

#from pyspark.sql.functions import countDistinct

#ifa_indexed_store_2 = ifa_indexed_store.select(countDistinct("ifa"))

#ifa_indexed_store_2.show()

#dfm_join_2 = dfm_join.select(countDistinct("ifa", "poiCode"))

#dfm_join_2.show()

# %%
#dfm_join_2 = dfm_join.select(countDistinct("ifa", "poiCode"))

#dfm_join_2.show()

#print(dfm_join.count())

# %%
#df_poi_2 = df_poi.select(countDistinct("poiCode", "h12"))

#df_poi_2.show()

#dfm_join_3 = dfm_join.select(countDistinct("poiCode", "h12"))

#dfm_join_3.show()

# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%
# print("TextFile : "+str(rddFromFile.getNumPartitions()))

# %%

# # # The following row avoids the broadcasting, the dimension_table2 is very small
# # spark.conf.set("spark.sql.autoBroadcastJoinThreshold",-1)

# # # // Using caching to simplify the DAG
# # dimension_table2.cache




# Option 1: we can try to repartition our fact table, in order to distribute the effort in the nodes



# fact_table = fact_table.repartition(400, fact_table.col("repartition_id"))

# fact_table = fact_table.join(dimension_table2.repartition(400, dimension_table2.col("repartition_id")), 
#                 fact_table.col("repartition_id") === dimension_table2.col("repartition_id"), "left")
# fact_table.count



# Option 2: we can artificially create a repartitioning key (key salting)


# %%


# %%


# %%


# %%

# ### saving to gold table
# ### test right partitioning and z-ordering to make faster query

# spark.sql("DROP TABLE  IF EXISTS poi_data")

# spark.sql("CREATE TABLE poi_data USING DELTA LOCATION " + save_string)
                  
# spark.sql("OPTIMIZE poi_data ZORDER BY (h6)") ### test - partition by h6/poiType/city



# %%
#dfx2 = spark.read.format('delta').load(save_string)

#dfx2.show()


# %%
#save to database

#10.0.1.188 - prod
#
if source =="ls":
    start_time = time.time()
    #engine=db.create_engine('mysql+pymysql://application:Infana123!@10.0.1.132:3306/test')



    #dfx1_pandas = dfx1.select("*").toPandas()

    #merged_renmaed_df = dfx1_pandas.rename(columns={"poiTypeId":"poiType"}, inplace=False)

    #merged_renmaed_df.to_sql('ifasDailyVisitation', con=engine, if_exists='append',index=False,chunksize=5000)

    log_str= "request_id="+token+";task_id=3.1;task_name=Write file to Database;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok"
    writeToLogs(log_str)
    

# %%
#save_string = "s3://ia-customer-insights/poi_data/US_data.csv"
#df_poi = spark.read.format("csv").load(save_string.split(','),header = True)
#df_poi.show(3)

# %%
#dfx1.count()

# %%
# 285120851

# %%
spark.stop()

# %%


# %%



