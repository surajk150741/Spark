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

spark = SparkSession.builder.appName("step_00") \
        .config("spark.default.parallelism", '120')\
        .config("spark.scheduler.mode", "FAIR") \
        .config("spark.pyspark.virtualenv.enabled", "true") \
        .config("spark.delta.logStore.oci.impl","io.delta.storage.OracleCloudLogStore")\
        .config("fs.oci.client.custom.authenticator", "com.oracle.bmc.hdfs.auth.InstancePrincipalsCustomAuthenticator")\
        .config('fs.oci.client.hostname', "https://objectstorage.us-ashburn-1.oraclecloud.com")\
        .config('fs.oci.client.auth.tenantId.region', "us-ashburn-1")\
        .getOrCreate()
#        .config("spark.driver.memory", "56g") \
#        .config("spark.driver.cores", "4") \
#        .config("spark.executor.memory", "20g") \
#        .config("spark.executor.cores", "2") \
#        .config("spark.executor.instances", '61')\
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
print("sparkContext")
print(spark.sparkContext._conf.getAll())
#print(ociconf)
print(spark.sparkContext.defaultParallelism)

# %%

####Arguments
date_start = str(sys.argv[1])#dbutils.widgets.get('date_start')
#days = (datetimutils.widgets.get('date_start')#"2021-12-09"
country = str(sys.argv[2])#dbutils.widgets.get('country')#"ARE"
today = (date.today()).strftime("yyyy-mm-dd")
source = "GRAVY"
unique_token = f"PROD_API_STEP_00_{today}_{date_start}_{country}_{source}"
####Arguments
token = requestId = "{}".format(unique_token)
#days = (datetime.now() - dt.datetime.strptime(date_start, "%Y-%m-%d")).days
str_arg = ""
tminus = dt.datetime.strptime(date_start, "%Y-%m-%d")#date.today() - timedelta(days=int(38))# 2021-04-12
print(tminus)
date_string = tminus.strftime('%d')
month_string = tminus.strftime('%m')
year_string  = tminus.strftime('%Y')
print(date_string)

str_arg  = str_arg+"start time="+str(datetime.now())+"\n"

# %%
namespace = "bmmp5bv7olp2"

signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
identity_client = oci.identity.IdentityClient(config={}, signer=signer)

def createLogs():
    
    try:
        f = BytesIO()
        FILE_PATH = ""
        more_binary_data = str(f.getvalue().decode()) + "request_id="+requestId+";notebook_name=Date wise Split for Vendor data;start_time="+str(time.time())+"\n request_id="+requestId+";message=Started Date wise split \n"
    #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
    # Method 1: Object.put()
        #validate_config(ociconf)
        bucket_name = "ia-mobility-logs"
        object_storage_client = ObjectStorageClient(signer=signer, config={})
        logs_path = 'logs/{0}/{2}/{1}_pre-process.txt'.format(str(tminus.strftime('%Y-%m-%d')), country, source)
        object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
        print("create logs completed")
    except Exception as e:
        print("create logs failed")
        print(e)
        
createLogs()

def writeToLogs(str_arg):
    try:
        f = BytesIO()
        bucket_name = "ia-mobility-logs"
        logs_path = 'logs/{0}/{2}/{1}_pre-process.txt'.format(str(tminus.strftime('%Y-%m-%d')), country, source)
        object_storage_client = ObjectStorageClient(signer=signer, config={})
        file_data = object_storage_client.get_object(namespace,bucket_name, logs_path)
        f.seek(0)
    
        more_binary_data =  str(file_data.data.text)+"\n"+"notebook_name=Date wise Split for Vendor data;" +  str(str_arg)
        #print(more_binary_data)
        #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
        # Method 1: Object.put()
        #logs_path = 'logs/{0}/{1}_pre-process.txt'.format(str(tminus.strftime('%Y-%m-%d')), country)
        object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
        return "completed"
    except Exception as e:
        print(e)
        return e

# %%
print('workkkkk')
def getPath(source):
    paths = {
        "gravy":{
        "source":f"oci://ia-location-data@bmmp5bv7olp2/gravyanalytics/datasets/daily/shared-{date_start}/countryCode={country}/*.csv.gz",
        "format":"csv",
            "delimiter":"|"
        },
        "ls":{
            "source":f"oci://ia-lifesight@bmmp5bv7olp2/dataset/Mobility/{year_string}/{month_string}/{date_string}/cnt={country}/*.parquet",
            "format":"parquet",
            
        }
        }
    return paths[source]

def getFiles(date_val, month_val):
    try:
        
        path =  getPath(source.lower())       
        #f"oci://mobility-data@bmmp5bv7olp2/USA-IND-MEX/gravy/daily/{year_string}/{month_string}/{date_string}/*.gz" 
        if path["delimiter"]:
            df = spark.read.option("delimiter", path["delimiter"]).format(path["format"]).load(path["source"], headers="true")
        else:
            df = spark.read.format(path["format"]).load(path["source"], headers="true")
            
        #parquet(paths)
        print(writeToLogs("request_id="+requestId+"message=File checking started. File found at following location;file_path="+path["source"]))
    except Exception as e:
        print(e)
        #path = f"s3://ia-lifesight/dataset/Mobility/{year_string}/"+month_string+"/"+date_string+"/*.parquet"
        #df = spark.read.parquet(path)
        print(writeToLogs("request_id="+requestId+"message=File checking started. File found at following location;file_path="+path["source"]))
        spark.stop()
    print(path)
    return df


df = getFiles(date_string,month_string)
#str_arg = str_arg + paths +"\n"

if "_c0" in df.columns:
    col_names = ['UUID', 'AAID', "latitude", "longitude", "timestamp", "time_zone", "IP_address", "forensic_flag", "device_type","record_count", "country", "browser"]
    df = df.toDF(*col_names)
     

start_time = time.time()
df0 = df#spark.read.parquet(paths)
print(df0.rdd.getNumPartitions())
df = df0#.repartition(13375)
#df.show(3)
log_str= "request_id="+requestId+";task_id=1.0;task_name=Read file from input;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
print(writeToLogs(log_str))

# %%
start_time = time.time()
#df.show(3)
df0 = df.filter(df.country == country)

df1 = df0.filter(df0.latitude != "0.0")
df1 = df1.filter(df1.longitude != "0.0")

log_str= "request_id="+requestId+";task_id=1.1;task_name=Remove incorrect lat, long;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
writeToLogs(log_str)


start_time = time.time()
#df2 = df1.withColumn("timestamp", df["timestamp"] / 1000)
df2 = df1.withColumn("timestamp", F.from_unixtime(F.col("timestamp"), 'yyyy-MM-dd HH:mm:ss').cast("timestamp"))
# df2.show()

from datetime import datetime
from dateutil import tz

def return_time(time):
  from_zone = tz.gettz('UTC')

  if(country == "IND"):
    to_zone = tz.gettz('Asia/Kolkata')
  elif(country == "ARE"):
    to_zone = tz.gettz('Asia/Dubai')
  elif(country == "MEX"):
    to_zone = tz.gettz('America/Mexico_City')
  else:
    to_zone = tz.gettz('UTC')
    writeToLogs("New Country")   

  utc = datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')
  utc = utc.replace(tzinfo=from_zone)

  central = utc.astimezone(to_zone)      
  return [str(central)[:-6]]

schema = StructType([
    StructField("time", StringType(), False)
])

loc_test = udf(lambda a: return_time(a), schema)

#df3 = df2.select('maid', 'id_type', 'latitude', 'longitude', 'horizontal_accuracy', 'vertical_accuracy', 'altitude', 'ipv4', 'ipv6', 'user_agent', 'country', 'state_hasc', 'city_hasc', 'postcode', 'geohash', 'hex8', 'hex9', #'heading', 'speed', 'wifi_ssid', 'wifi_bssid', 'carrier', loc_test('timestamp').alias('indexTime'))

#df3 = df3.select('maid', 'id_type', 'latitude', 'longitude', 'horizontal_accuracy', 'vertical_accuracy', 'altitude', 'ipv4', 'ipv6', 'user_agent', 'country', 'state_hasc', 'city_hasc', 'postcode', 'geohash', 'hex8', 'hex9', #'heading', 'speed', 'wifi_ssid', 'wifi_bssid', 'carrier', 'indexTime.time')

#df3 = df3.selectExpr('maid as maid', 'id_type as id_type', 'latitude as latitude', 'longitude as longitude', 'horizontal_accuracy as horizontal_accuracy', 'vertical_accuracy as vertical_accuracy', 'altitude as altitude', #'ipv4 as ipv4', 'ipv6 as ipv6', 'user_agent as user_agent', 'country as country', 'state_hasc as state_hasc', 'city_hasc as city_hasc', 'postcode as postcode', 'geohash as geohash', 'hex8 as hex8', 'hex9 as hex9', 'heading #as heading', 'speed as speed', 'wifi_ssid as wifi_ssid', 'wifi_bssid as wifi_bssid', 'carrier as carrier', 'time as timestamp')
#if "time_zone" not in df2.columns:

#df3 = df2.withColumn("country", lit(country)).withColumn("converted_ts", when(col("country") == 'ARE', from_utc_timestamp(col("timestamp"), "Asia/Dubai")).otherwise(when(col("country") == 'IND', from_utc_timestamp(col("timestamp"), "Asia/Kolkata")).otherwise(from_utc_timestamp(col("timestamp"), "UTC"))))
#else:
#    df3 = df2.withColumn("converted_ts", from_utc_timestamp(col("timestamp"), col("time_zone")))
df3 = df2.withColumn("timestamp", F.from_utc_timestamp(F.from_unixtime(F.col("timestamp").cast("bigint")/1000, 'yyyy-MM-dd HH:mm:ss').cast("timestamp"), F.col("time_zone")))
df3 = df3.withColumn('date', F.to_date(col('timestamp')).cast("date"))

from pyspark.sql.functions import *
#df3 = df3.withColumn("timestamp", to_timestamp("timestamp", "yyyy-MM-dd HH:mm:ss"))
# df3.show(3)


log_str= "request_id="+requestId+";task_id=1.2;task_name=Convert date time;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
print(writeToLogs(log_str))


#percent_data_spill.show()

#date_values = dates.select('date').collect()

def filterOutDate(date_val):
    df4 = df3.filter(df3.date == date_val)
    df4.show(3)

folder_date = tminus.strftime('%Y-%m-%d')




# %%
save_string = f"oci://ia-visitation-data@bmmp5bv7olp2/{source.lower()}_data/hdfs_data/step_0_new/{country}/"
str_arg = str_arg+"files_path="+save_string+"\n"


# %%
start_time = time.time()
numPartitions = 76
newDF = df3#.repartition(numPartitions)
newDF = newDF.withColumn("year", newDF.date.substr(1,4))
#newDF.show(3)
log_str= "request_id="+requestId+";task_id=2.0;task_name=Repartition data;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
print(writeToLogs(log_str))

# %%
start_time = time.time()
try:
    newDF.write.partitionBy(['year','date']).mode("append").format('delta').save(save_string)
    log_str= "request_id="+requestId+";task_id=2.1;task_name=Write to S3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)
except Exception as e:
    log_str= "request_id="+requestId+";task_id=2.1;task_name=Write to s3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=fail;message=error;error_message="+str(e) 
    writeToLogs(log_str)

# %%
#df3.show(3)

total_rows = df3.count()
print(total_rows)

total_valid_rows = df3.count()
print(total_valid_rows)

str_arg = str_arg + "total_rows="+str(total_rows)+"\n"+"total_valid_rows="+\
          str(total_valid_rows)+"\n"

if(total_rows == total_valid_rows):
    str_arg = str_arg + "rows count equal \n"
else: 
    str_arg = str_arg+"rows count not equal \n"

dates = df3.groupby('date').count()

#dates.sort('date').show()
percent_data_spill = dates.withColumn('percent', (col("count")/total_valid_rows)*100.0)

analytics_save_path = f"oci://ia-mobility-logs@bmmp5bv7olp2/logs/{source}/Analytics/"+str(tminus.strftime("%Y-%m-%d"))+".csv"

text_string=""

for x in percent_data_spill.sort('date').collect():
    text_string = text_string +"total_rows="+str(total_rows)+",total_valid_rows="+\
    str(total_valid_rows)+\
    ",date="+str(x[0])+",user_row="+str(x[1])+",percentage="+"{0:.2f}".format(x[2])+\
    ",received_date="+str(tminus.strftime('%Y-%m-%d'))+"\n"

print(text_string)

log_str= "request_id="+requestId+";task_id=2.2;task_name=File execution completed;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok"
writeToLogs(log_str) 


file_path =  'analytics/{1}/{0}/analysis.txt'.format(str(tminus.strftime('%Y-%m-%d')), source)

object_storage_client = ObjectStorageClient(signer=signer, config={})
object_storage_client.put_object(namespace, 'ia-mobility-logs', file_path, put_object_body=log_str)




# %%
spark.stop()

