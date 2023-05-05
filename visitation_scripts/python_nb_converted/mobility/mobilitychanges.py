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

spark = SparkSession.builder.appName("mobility_changes") \
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



##Arguments##
#date_start="2021-05-02"
#date_end ="2021-05-02"
#days="5"
#token="generic_mobility_0502"
#input_state = "MH"
#input_date = "2021-05-02"
# source_data_path="s3://ia-customer-insights/lf_data/hdfs_data/lf/Updated_May15.csv.gz"
#source_data_path = "s3://ia-customer-insights/lf_data/hdfs_data/ls/IN/date=2021-05-02/"
# source_data_path = "s3://ia-customer-insights/lf_data/hdfs_data/ls/IN/date={}/state={}".format(input_date, input_state)

from typing import Counter

input_date = sys.argv[1]
unique_token = sys.argv[2]#"06072021"
country = sys.argv[3]#"IND"
dataset_name = sys.argv[4]#"LS"
source_data_path = f"oci://ia-visitation-data@bmmp5bv7olp2/mobility/lf_data/hdfs_data/{dataset_name.lower()}/parquet/step_1/"
#"s3://ia-customer-insights/lf_data/hdfs_data/ls/{}/date={}/".format(country, input_date)

# polygon_data_path = "s3://ia-customer-insights/required_files/state_city_h3_mapping.csv.gz"
##Arguments##


# polygon_data_path = "s3://ia-customer-insights/required_files/state_county_h3_mapping.csv.gz,s3://ia-customer-insights/required_files/state_city_h3_mapping.csv.gz"
h3_index_resolution = "idx9"
h3_resolution = "9"
###### ARGUMENTS

days = (datetime.now() - dt.datetime.strptime(input_date, "%Y-%m-%d")).days
tminus = date.today() - timedelta(days=int(days))
print(tminus)
date_string = tminus.strftime('%B%d')
print(date_string)

# token_date = date_string.strftime('%B_%d')
#token = requestId = "{}_{}".format(input_date, unique_token)
token = requestId = unique_token

print(token, date_string)
# --------------------------------------------------------------------------------

def _get_polygon_data(country):
        if country == 'IND':
            return 'oci://ia-customer-insights@bmmp5bv7olp2/required_files/state_city_h3_mapping.csv.gz'
        elif country == 'USA':
            return 'oci://ia-customer-insights@bmmp5bv7olp2/required_files/state_county_h3_mapping.csv.gz'
        elif country == 'ARE':
            return 'oci://ia-customer-insights@bmmp5bv7olp2/required_files/are_polygons.csv'
        else:
            ValueError('Country `{}` data does not exist, existing countries are IND,US,ARE.')

polygon_data_path = _get_polygon_data(country=country)
namespace = "bmmp5bv7olp2"

signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
identity_client = oci.identity.IdentityClient(config={}, signer=signer)

def createLogs():
    try:
        f = BytesIO()

        more_binary_data = str(f.getvalue().decode()) + "request_id="+requestId+";notebook_name=Raw Mobility Changes;start_time="+str(time.time())+";message=Started Mobility Changes generation\n"
        #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
        # Method 1: Object.put()
        #s3 = boto3.resource('s3')
        #object = s3.Object('ia-mobility-logs', logs_path)
        #object.put(Body=more_binary_data)
        #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
        # Method 1: Object.put()
        #validate_config(ociconf)
        bucket_name = "ia-mobility-logs"
        object_storage_client = ObjectStorageClient(signer=signer, config={})
        logs_path = "log/{0}/{1}_part_1_mobility_script_generic.txt".format(str(country),str(input_date))
        object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
        print("create logs completed")

    except Exception as e:
        print(e)

createLogs()

def writeToLogs(str_arg):
    
    try:
        f = BytesIO()

        bucket_name = "ia-mobility-logs"
        logs_path = "log/{0}/{1}_part_1_mobility_script_generic.txt".format(str(country),str(input_date))

        object_storage_client = ObjectStorageClient(signer=signer, config={})
        file_data = object_storage_client.get_object(namespace,bucket_name, logs_path)
        f.seek(0)
        more_binary_data = str(file_data.data.text) +"notebook_name=Raw Mobility Changes;"+str(str_arg)+"\n"
        object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
        return "completed"
    except Exception as e:
        print(e)

# source_data_path = "s3://ia-customer-insights/lf_data/hdfs_data/lf/Updated_"+date_string+".csv.gz"
# source_data_path = "s3://ia-customer-insights/lf_data/hdfs_data/lf/March17.csv.gz,s3://ia-customer-insights/lf_data/hdfs_data/lf/March18.csv.gz,s3://ia-customer-insights/lf_data/hdfs_data/lf/March19.csv.gz,s3://ia-customer-insights/lf_data/hdfs_data/lf/March20.csv.gz,s3://ia-customer-insights/lf_data/hdfs_data/lf/March21.csv.gz"

# --------------------------------------------------------------------------------
# token_string = "_US_2_sample_generic_"
# token_date = datetime.today().strftime('%B_%d')
# token = "_"+token_date + token_string

# --------------------------------------------------------------------------------
# token = dbutils.widgets.get("token")
# date_string = dbutils.widgets.get("date_string")
# date_start = dbutils.widgets.get("date_start")
# date_end = dbutils.widgets.get("date_end")
# dataset_name = dbutils.widgets.get("dataset_name")
# source_data_path = dbutils.widgets.get("source_data_path")
# # polygon_data_path = dbutils.widgets.get("polygon_data_path")
# h3_index_resolution = dbutils.widgets.get("h3_index_resolution")
# h3_resolution = dbutils.widgets.get("h3_resolution")
# log_file_name = "/generic_mobility/logs/part_1_mobility_script_generic.log"
# log_file_name = "/generic_mobility/logs/all_processes.log"
# log_file_path = "/dbfs" + log_file_name
str_arg = ""
# -------------------------------
cmd_time = time.time()
utc_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# -------------------------------  
arguments = "notebook_name="+ "part_1_mobility_script_generic" + ";"+ "Executing the script...." +"\n"
str_arg += arguments
# sc = SparkSession.builder.master("local").appName("sample").getOrCreate()
# sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
# sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")

# sc._jsc.hadoopConfiguration().set("fs.s3a.awsAccessKeyId", accessKeyId)
# sc._jsc.hadoopConfiguration().set("fs.s3a.awsSecretAccessKey", secretAccessKey)

arguments =  "notebook_name="+ "part_1_mobility_script_generic" + ";"+ "dataset_name="+ dataset_name + ";input_date="+ input_date + ";token="+ token  + ";country="+ country  +  ";utc_start_time="+ utc_start_time +"\n"
print("arguments - " ,arguments)
str_arg += arguments
start_time = time.time()
polygon_data = spark.read.format('csv').load(polygon_data_path.split(','), header = 'true')
log_str= "request_id="+requestId+";task_id=1.0;task_name=Read polygon index data;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
writeToLogs(log_str)
polygon_data = polygon_data.selectExpr("country as country", "state as state", "city as p_city", "idx9 as idx9")
polygon_data.show(3)
# ifa_indexed_store2 = spark.read.format("csv").load(source_data_path.split(','), header = 'true')
# ifa_indexed_store2.show(6)
# ifa_indexed_store2 = spark.read.format("parquet").load(source_data_path.split(','), header = 'true')
start_time = time.time()
df0 = spark.read.parquet(source_data_path).where(f"'date' == '{input_date}'")
log_str= "request_id="+requestId+";task_id=1.1;task_name=Read file from input;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
writeToLogs(log_str)
start_time= time.time()
numPartitions = 800
ifa_indexed_store2 = df0.repartition(numPartitions)
ifa_indexed_store2.columns
ifa_indexed_store2.show(6)
log_str= "request_id="+requestId+";task_id=1.1;task_name=Repartition data;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
writeToLogs(log_str)
df_cols = ifa_indexed_store2.columns
if "date" not in df_cols:
    ifa_indexed_store2 = ifa_indexed_store2.withColumn("date", lit(input_date))
if "state" not in df_cols:
    ifa_indexed_store2 = ifa_indexed_store2.withColumn("state", lit(input_state))
# ifa_indexed_store2 = ifa_indexed_store2.selectExpr("_c0 as user_id", "_c1 as city" , "_c8 as zip", "_c8 as carrier", "_c2 as date", "_c3 as lat","_c4 as long", "_c5 as timestamp", "_c6 as status", "_c7 as reliable_city")
ifa_indexed_store2 = ifa_indexed_store2.select('ifa', 'city', 'zip', 'carrier', 'date', 'lat', 'long', 'timestamp')
ifa_indexed_store2 = ifa_indexed_store2.withColumnRenamed("ifa","user_id")
    
ifa_indexed_store2 = ifa_indexed_store2.withColumn("reliable_city", ifa_indexed_store2["city"])
# ifa_indexed_store2.count()
# ifa_indexed_store2.show(3)
sample_lag = ifa_indexed_store2.withColumn('lat_lag', func.lag(ifa_indexed_store2['lat']).over(Window.partitionBy(["date","reliable_city","user_id"]).orderBy(func.col("timestamp").desc())))
sample_lag = sample_lag.withColumn('long_lag', func.lag(sample_lag['long']).over(Window.partitionBy(["date","reliable_city","user_id"]).orderBy(func.col("timestamp").desc())))
sample_lag = sample_lag.withColumn('timestamp_lag', func.lag(sample_lag['timestamp']).over(Window.partitionBy(["date","reliable_city","user_id"]).orderBy(func.col("timestamp").desc())))
if(country == "ARE"):
    sample_lag = sample_lag.withColumn("zip", lit("0"))
sample_lag = sample_lag.na.drop()
# sample_lag.show(5)
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = float(lon1), float(lat1), float(lon2), float(lat2)
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return [str(c * r * 1000)]  
schema = StructType([
    StructField("dist", StringType(), False)
])
loc_test = udf(lambda a,b,c,d: calculate_distance(a,b,c,d), schema)
start_time = time.time()
ifa_indexed = sample_lag.select('user_id', 'city', 'lat','long', 'carrier', 'date', 'lat_lag', 'long_lag', loc_test('lat','long', 'lat_lag', 'long_lag').alias('delta'), 'zip', 'timestamp', 'timestamp_lag')
ifa_indexed_store = ifa_indexed.select("user_id", "city", "lat", "long", "lat_lag", "long_lag", "carrier", "date", "delta.dist", "zip", "timestamp", "timestamp_lag")
# ifa_indexed_store.show(3)
log_str= "request_id="+requestId+";task_id=2.0;task_name=Calculate distance;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
writeToLogs(log_str)

filtered_dates = ifa_indexed_store.filter(ifa_indexed_store.timestamp.contains(input_date))
rows_issue_count=ifa_indexed_store.count()-filtered_dates.count()
log_str= "request_id="+requestId+";task_id=2.0.1;task_name=Issues with timestamp rows="+str(rows_issue_count)+";task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
     ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
writeToLogs(log_str)

ifa_indexed_store = ifa_indexed_store.filter(ifa_indexed_store.timestamp.contains(input_date))

def calculate_distance(time_prev, time_next):
    try: 
        time1 = time_prev
        time2 = time_next
        time_delta = (time2 - time1).total_seconds()/60
    except Exception as e:    
        time1 = dt.datetime.strptime(time_prev, '%Y-%m-%d %H:%M:%S')
        time2 = dt.datetime.strptime(time_next, '%Y-%m-%d %H:%M:%S')
        time_delta = (time2 - time1).total_seconds()/60
    
    return [str(time_delta)]
schema = StructType([
    StructField("time", StringType(), False)
])
loc_test2 = udf(lambda a,b: calculate_distance(a,b), schema)
start_time = time.time()
ifa_indexed2 = ifa_indexed_store.select('user_id', 'city', 'lat','long', 'carrier', 'date', 'lat_lag', 'long_lag', 'dist', 'timestamp', 'timestamp_lag', loc_test2('timestamp','timestamp_lag').alias('tdelta'), 'zip')
ifa_indexed_store2 = ifa_indexed2.select("user_id", "city", "lat", "long", "lat_lag", "long_lag", "dist", "carrier", "date", "tdelta.time", "zip", "timestamp", "timestamp_lag")
ifa_indexed_store2.show(3)
log_str= "request_id="+requestId+";task_id=2.1;task_name=Calculate time;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
writeToLogs(log_str)
# ifa_indexed_store2.show(3)
save_string_4 = "s3://ia-customer-insights/Intermediate_data/" + token +".parquet.gz"
#print(save_string_4)
start_time = time.time()
try:
    ifa_indexed_store2.write.format("parquet").mode('overwrite').save(save_string_4)
    log_str= "request_id="+requestId+";task_id=2.2;task_name=write to Intermediate on S3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)
except Exception as e:
    log_str= "request_id="+requestId+";task_id=2.2;task_name=write to Intermediate on S3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=error;message=fail;error_message="+ str(e) 
    writeToLogs(log_str)
# ifa_indexed_store2.show(3)
ifa_indexed_store2 = spark.read.format('parquet').load(save_string_4)
# ifa_indexed_store2 = ifa_indexed_store2.selectExpr("_c0 as user_id", "_c1 as city", "_c2 as lat" , "_c3 as long", "_c4 as lat_lag", "_c5 as long_lag", "_c6 as tot_dist", "_c7 as carrier", "_c8 as date", "_c9 as tot_time", "_c10 as zip", "_c11 as timestamp", "_c12 as timestamp_lag")
ifa_indexed_store2.show(6)
def return_index(lat, long):
    try:
        return [h3.geo_to_h3(float(lat), float(long), 7), h3.geo_to_h3(float(lat), float(long), 8), h3.geo_to_h3(float(lat), float(long), 9), h3.geo_to_h3(float(lat), float(long), 10), h3.geo_to_h3(float(lat), float(long), 11), h3.geo_to_h3(float(lat), float(long), 12)]
    except Exception as error:
        return ["0", "0", "0", "0","0","0"]
schema = StructType([
    StructField("idx7", StringType(), False),
    StructField("idx8", StringType(), False),
    StructField("idx9", StringType(), False),
    StructField("idx10", StringType(), False),
    StructField("idx11", StringType(), False),
    StructField("idx12", StringType(), False)  
])
loc_test = udf(lambda a,b: return_index(a,b), schema)
ifa_indexed_store2 = ifa_indexed_store2.withColumnRenamed("dist","tot_dist")    
ifa_indexed_store2 = ifa_indexed_store2.withColumnRenamed("time","tot_time")    
start_time = time.time()
ifa_indexed = ifa_indexed_store2.select('user_id', 'lat','long', 'lat_lag', 'long_lag', 'tot_dist', 'date', loc_test('lat','long').alias('indexH3'), 'carrier', 'zip', 'tot_time', 'timestamp', 'timestamp_lag', 'city')
ifa_indexed_store = ifa_indexed.select("user_id", "lat", "long", "lat_lag", "long_lag", "tot_dist", "date", "indexH3.idx7", "indexH3.idx8", "indexH3.idx9", "indexH3.idx10","indexH3.idx11","indexH3.idx12","carrier", "zip", "tot_time", "timestamp", "timestamp_lag", "city")
ifa_indexed_store.show()
log_str= "request_id="+requestId+";task_id=2.3;task_name=Create variable index;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=ok;message=sucess;" 
writeToLogs(log_str)
mobility_union = ifa_indexed_store.join(polygon_data, on=[h3_index_resolution], how='inner')
#### **************
# mobility_union.show(3)
#print(mobility_union.columns)
mobility_union = mobility_union.select('idx9', 'user_id', 'lat', 'long', 'lat_lag', 'long_lag', 'tot_dist', 'date', 'idx7', 'idx8', 'idx10', 'idx11', 'idx12', 'carrier', 'zip', 'tot_time', 'timestamp', 'timestamp_lag', 'city' ,"state")
save_string_4_2 = "s3://ia-customer-insights/Intermediate_data/" + token +"_with_h9_.parquet.gz"
#print(save_string_4_2)
start_time = time.time()
try:
    mobility_union.write.format("parquet").mode('overwrite').save(save_string_4_2, header = 'true')
    log_str= "request_id="+requestId+";task_id=2.4;task_name=write to Intermediate on S3 for Variable index;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
    writeToLogs(log_str)
except Exception as e:
    log_str= "request_id="+requestId+";task_id=2.4;task_name=write to Intermediate on S3 for Variable index;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=error;message=fail;error_message="+ str(e) 
    writeToLogs(log_str)
# save_string_4_2 = "s3://ia-customer-insights/Intermediate_data/generic_mobility_111_with_h9_.csv.gz"
mobility_union = spark.read.format('parquet').load(save_string_4_2)
# mobility_union = mobility_union.selectExpr("_c0 as idx9","_c1 as user_id","_c2 as lat","_c3 as long","_c4 as lat_lag","_c5 as long_lag","_c6 as tot_dist","_c7 as date","_c8 as idx7","_c9 as idx8","_c10 as idx10","_c11 as idx11","_c12 as idx12","_c13 as carrier","_c14 as zip","_c15 as tot_time","_c16 as timestamp","_c17 as timestamp_lag","_c18 as city","_c19 as id1","_c20 as id2","_c21 as district")
mobility_union.show(5)
if (dataset_name != "MW"):
    start_time = time.time()
    mobility_union = mobility_union.withColumnRenamed("district","city")    
    mobility = mobility_union.groupBy(["date","user_id"]).agg(F.sum("tot_dist").alias("all_dist_sum"), F.sum("tot_time").alias("all_time_sum")) 
    static_users = mobility.filter(mobility.all_dist_sum < 10)
    static_users.select('date','user_id').show(3)
    start_time = time.time()
    mobility_union_agg_by_hex = mobility_union.groupBy(["date","state","city","user_id", h3_index_resolution]).agg(F.sum("tot_dist").alias("all_dist_sum"), F.sum("tot_time").alias("all_time_sum"))
    mobility_union_agg_moving = mobility_union_agg_by_hex.filter(mobility_union_agg_by_hex.all_dist_sum > 10)
    mobility_union_agg_moving.show(5)
    log_str= "request_id="+requestId+";task_id=3.0;task_name=Calculate moving users;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
    writeToLogs(log_str)
    start_time = time.time()
    mobility_union_static = mobility_union.join(static_users, on=["date", "user_id"], how='inner')
    mobility_union_agg_by_hex = mobility_union_static.groupBy(["date","state","city","user_id", h3_index_resolution]).agg(F.sum("tot_dist").alias("all_dist_sum"), F.sum("tot_time").alias("all_time_sum"))
    mobility_union_agg_static = mobility_union_agg_by_hex.filter(mobility_union_agg_by_hex.all_dist_sum < 10)
    mobility_union_agg_static.show(5)
    log_str= "request_id="+requestId+";task_id=3.1;task_name=Calculate static user;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
    writeToLogs(log_str)
    by_hex_count_moving = mobility_union_agg_moving.groupBy(["date","state","city", h3_index_resolution]).agg(F.sum("all_dist_sum").alias("all_dist_sum"), F.sum("all_time_sum").alias("all_time_sum"), F.count("all_dist_sum").alias("all_count_moving")).orderBy(["date","state","city"], ascending=True)
    # mobility_union_agg_by_hex.filter(mobility_union_agg_by_hex.all_count > 25).show()
    # by_hex_count_moving.show()
    
    by_hex_count_static = mobility_union_agg_static.groupBy(["date","state","city", h3_index_resolution]).agg(F.sum("all_dist_sum").alias("all_dist_sum"), F.sum("all_time_sum").alias("all_time_sum"), F.countDistinct("user_id").alias("all_count_static")).orderBy(["date","state","city"], ascending=True)
    # mobility_union_agg_by_hex.filter(mobility_union_agg_by_hex.all_count > 25).show()
    # by_hex_count_static.show()  
    
    finaly_agg_by_hex = by_hex_count_moving.join(by_hex_count_static.select('date', "state",'city', 'idx9', 'all_count_static'), on=["date","state","city", h3_index_resolution], how='left')      #### **************
    # finaly_agg_by_hex = finaly_agg_by_hex.select("date","district",h3_index_resolution,"all_dist_sum","all_time_sum","all_count","all_count_static")
    finaly_agg_by_hex = finaly_agg_by_hex.fillna({'all_count_static':'0'})
    #finaly_agg_by_hex.show(30)
    
    
# by_hex_count_moving.join(by_hex_count_static.select('date', "state",'city', 'idx9', 'all_count_static'), on=["date","state","city", h3_index_resolution], how='inner').show()      #### **************
# by_hex_count_moving.join(by_hex_count_static.select('date', "state",'city', 'idx9', 'all_count_static'), on=["date","state","city", h3_index_resolution], how='left').show()      #### **************
#finaly_agg_by_hex.show(3)
save_string_5 = "s3://ia-customer-insights/Intermediate_data/mobility_analysis_" + dataset_name + token +"_by_hex_.parquet.gz"
#print(save_string_5)
start_time = time.time()
try:
    finaly_agg_by_hex.write.format("parquet").mode('overwrite').save(save_string_5, header = "true")
    log_str= "request_id="+requestId+";task_id=3.3;task_name=Wriet Intermediate date to S3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
    writeToLogs(log_str)
except Exception as e:
    log_str= "request_id="+requestId+";task_id=3.1;task_name=Calculate ;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=error;message=fail;error_message="+str(e) 
    writeToLogs(log_str)
# save_string_5 = "abfss://contact-tracing@iasocialdata.dfs.core.windows.net/contact_tracing/Intermediate_data/mobility_analysis_ISA_INgeneric_mobility_301_by_hex_.csv.gz"
finaly_agg_by_hex = spark.read.format('parquet').load(save_string_5)
block_path = "oci://ia-visitation-data@bmmp5bv7olp2/contact_tracing/"+ dataset_name +"/delta/mobility_reports/district_block/"
#"s3://ia-customer-insights/contact_tracing/"+ dataset_name +"/mobility_reports/district_block/"+country+"/Updated_" + input_date + "_block_col.parquet"
# save_string_6 = "abfss://customer-insights@iasocialdata.dfs.core.windows.net/Shubham_data/all_india_mobility_analysis" + date_string +"_block.csv.gz"
#print(block_path)
# finaly_agg_by_hex = finaly_agg_by_hex.selectExpr("_c0 as date", "_c3 as h3index", "_c1 as state","_c2 as city", "_c4 as distance" , "_c5 as time", "_c7 as static", "_c6 as moving", "_c3 as poiCode")      #### **************
finaly_agg_by_hex.show(3)
start_time = time.time()
finaly_agg_by_hex = finaly_agg_by_hex.withColumnRenamed("all_dist_sum","distance")
finaly_agg_by_hex = finaly_agg_by_hex.withColumnRenamed("all_time_sum","time")
finaly_agg_by_hex = finaly_agg_by_hex.withColumnRenamed("all_count_moving","static")
finaly_agg_by_hex = finaly_agg_by_hex.withColumnRenamed("all_count_static","moving")
finaly_agg_by_hex = finaly_agg_by_hex.withColumnRenamed("idx9","h3index")
finaly_agg_by_hex = finaly_agg_by_hex.withColumn("poiCode", finaly_agg_by_hex["h3index"])
finaly_agg_by_hex = finaly_agg_by_hex.withColumn('distance', finaly_agg_by_hex.distance.cast(DecimalType(14, 2)))                              
finaly_agg_by_hex = finaly_agg_by_hex.withColumn('time', finaly_agg_by_hex.time.cast(DecimalType(14, 2)))                              
finaly_agg_by_hex = finaly_agg_by_hex.withColumn('static', finaly_agg_by_hex.static.cast(DecimalType(14, 2)))                              
finaly_agg_by_hex = finaly_agg_by_hex.withColumn('moving', finaly_agg_by_hex.moving.cast(DecimalType(14, 2)))   
#finaly_agg_by_hex = finaly_agg_by_hex.withColumn('poiType', lit("District.Block"))
finaly_agg_by_hex = finaly_agg_by_hex.withColumn('poiType', lit("admin.district_block"))
#finaly_agg_by_hex = finaly_agg_by_hex.filter(col("date").between(date_start, date_end))
# finaly_agg_by_hex.show(3)
finaly_agg_by_hex_rank = finaly_agg_by_hex.withColumn("rank", dense_rank().over(Window.partitionBy(["date","h3index"]).orderBy(desc("moving"))))
finaly_agg_by_hex_rank1 = finaly_agg_by_hex_rank.filter(finaly_agg_by_hex_rank.rank == "1")
# finaly_agg_by_hex_rank1 = finaly_agg_by_hex_rank1.withColumn('source', lit(dataset_name))
#finaly_agg_by_hex_rank1.show(3)
finaly_agg_by_hex_rank1 = finaly_agg_by_hex_rank1.select('date', 'h3index', 'state','city', 'distance', 'time', 'static', 'moving', 'poiCode', 'poiType')
finaly_agg_by_hex_rank1 = finaly_agg_by_hex_rank1.withColumn('source', lit(dataset_name))
finaly_agg_by_hex_rank1.show(3)
finaly_agg_by_hex_rank1 = finaly_agg_by_hex_rank1.withColumn("country", lit(country))
log_str= "request_id="+requestId+";task_id=4.0;task_name=rename columns;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
writeToLogs(log_str)
# finaly_agg_by_hex_rank1 = finaly_agg_by_hex_rank1.filter(col("state") == input_state)
start_time = time.time()
try:
    finaly_agg_by_hex_rank1.write.partitionBy(["country", "date"]).format("delta").mode('append').save(block_path, header = "true")
    log_str= "request_id="+requestId+";task_id=4.1;task_name=Write Distrist block data to s3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
    writeToLogs(log_str)
except Exception as e:
    log_str= "request_id="+requestId+";task_id=4.1;task_name=Write Distrist block data to s3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=error;message=fail;error_message="+str(e) 
    writeToLogs(log_str)
# block_path = "s3://ia-customer-insights/contact_tracing/"+ dataset_name +"/mobility_reports/district_block/Updated_" + input_date + "_block_col.parquet"
# finaly_agg_by_hex_rank1 = spark.read.format('parquet').load(block_path)
finaly_agg_by_hex_rank1.columns
start_time = time.time()
h3index_count = finaly_agg_by_hex_rank1.groupBy("h3index").count() #2014505
h3index_count = h3index_count.filter(col('count') < 2)
mobility_h3index_count = finaly_agg_by_hex_rank1.join(h3index_count.select("h3index"), on=["h3index"], how='inner')
# mobility_h3index_count.show(5)
# mobility_h3index_count.select("h3index").distinct().count()
# mobility_h3index_count.select("h3index").count()
finaly_agg_by_hex_rank1 = mobility_h3index_count.select('date', 'h3index', 'state', 'city', 'distance', 'time', 'static', 'moving', 'poiCode', 'poiType', 'source')
finaly_agg_by_hex_rank1.show(5)
log_str= "request_id="+requestId+";task_id=4.2;task_name=Calculate value for District Aggregate;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
writeToLogs(log_str)
start_time = time.time()
#save to database
#try:
#    block_df = finaly_agg_by_hex_rank1.select("*").toPandas()
#    block_df.to_sql('MobilityChanges', con=engine, if_exists='append',index=False,chunksize=5000)
#    log_str= "request_id="+requestId+";task_id=4.3;task_name=Ingest to database District block;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
#        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
#    writeToLogs(log_str)
#except Exception as e:
#    log_str= "request_id="+requestId+";task_id=4.3;task_name=Ingest to database District block;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
#        ";task_time_taken="+str(time.time()-start_time)+";status=fail;message=error;error_message="+str(e) 
#    writeToLogs(log_str) 
   
# final2 = finaly_agg_by_hex_rank1.filter(col("state") != 'MH')
# finaly_agg_by_hex_rank1.select("h3index").count()
# finaly_agg_by_hex_rank1.select("h3index").distinct().count()
# save_string_5 = "s3://ia-customer-insights/Intermediate_data/mobility_analysis_" + dataset_name + token +"_by_hex_.parquet.gz"
by_district = spark.read.format('parquet').load(save_string_5)
start_time = time.time()
# by_district = by_district.selectExpr("_c0 as date", "_c3 as h3index", "_c1 as state" ,"_c2 as city", "_c4 as distance" , "_c5 as time", "_c7 as static", "_c6 as moving")      #### **************
by_district = by_district.withColumnRenamed("all_dist_sum","distance")
by_district = by_district.withColumnRenamed("all_time_sum","time")
by_district = by_district.withColumnRenamed("all_count_moving","static")
by_district = by_district.withColumnRenamed("all_count_static","moving")
by_district = by_district.withColumnRenamed("idx9","h3index")
#by_district = by_district.withColumn('poiType', lit("District.Aggregate"))
by_district = by_district.withColumn('poiType', lit("admin.district_aggregate"))
#by_district = by_district.filter(col("date").between(date_start, date_end))
#by_district.show()
mobility_union_agg_district = by_district.groupBy(["date",'state','city','poiType']).agg(F.sum("distance").alias("distance"), F.sum("time").alias("time"), F.sum("static").alias("static"), F.sum("moving").alias("moving")).orderBy(["date"], ascending=True) 
#mobility_union_agg_district.show(3)
final2 = mobility_union_agg_district.select('date', 'city', 'state', 'distance', 'time', 'static', 'moving', 'poiType')
final2 = final2.withColumn("poiCode", final2["city"])
# final2.show(5)
final2 = final2.withColumn('distance', final2.distance.cast(DecimalType(14, 2)))                              
final2 = final2.withColumn('time', final2.time.cast(DecimalType(14, 2)))                              
final2 = final2.withColumn('static', final2.static.cast(DecimalType(14, 2)))                              
final2 = final2.withColumn('moving', final2.moving.cast(DecimalType(14, 2)))
final2 = final2.withColumn('source', lit(dataset_name))
final2.show(6)
log_str= "request_id="+requestId+";task_id=4.4;task_name=Rename column for district aggregate;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
writeToLogs(log_str)
final3 = final2.withColumn("rank", dense_rank().over(Window.partitionBy(["date","poiCode"]).orderBy(desc("moving"))))
final3 = final3.filter(final3.rank == "1")
# final3.select("poiCode").distinct().count()
# final3.select("poiCode").count()
# final3.filter(col("city") == "IN.MH.MC").show(5)
# save_string_7 = "s3://ia-customer-insights/Intermediate_data/" + token +"_by_city.csv.gz"
aggregate_path = "oci://ia-visitation-data@bmmp5bv7olp2/contact_tracing/"+ dataset_name +"/delta/mobility_reports/district_aggregate/"
#"s3://ia-customer-insights/contact_tracing/"+ dataset_name +"/mobility_reports/district_aggregate/"+country+"/Updated_" + input_date + "_aggregate_col.parquet" 
#print(save_string_7)
# final2 = final2.filter(col("state") == input_state)
final3 = final3.select('date', 'city', 'state', 'distance', 'time', 'static', 'moving', 'poiType', 'poiCode', 'source')
final3 = final3.withColumn("country", lit(country))
start_time = time.time()
try:
    final3.write.partitionBy(["country","date"]).format("delta").mode('append').save(aggregate_path, header = "true")
    log_str= "request_id="+requestId+";task_id=4.5;task_name=Write to S3 District Aggregate;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
    writeToLogs(log_str)
except Exception as e:
    log_str= "request_id="+requestId+";task_id=4.5;task_name=Write to S3 District Aggregatek;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
        ";task_time_taken="+str(time.time()-start_time)+";status=fail;message=error;error_message="+ str(e) 
    writeToLogs(log_str)
final3.show(10)
start_time = time.time()

print("Completed mobilitychanges")
#save to database
#try:
#    aggregate_df = final3.select("*").toPandas()
#    aggregate_df.to_sql('MobilityChanges', con=engine, if_exists='append',index=False,chunksize=5000)
#    log_str= "request_id="+requestId+";task_id=4.6;task_name=Ingest to database District Aggregate;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
#        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=ok" 
#    writeToLogs(log_str)
#except Exception as e:
#    log_str= "request_id="+requestId+";task_id=4.6;task_name=Ingest to database District Aggregate;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
#        ";task_time_taken="+str(time.time()-start_time)+";status=success;message=" + str(e) 
#    writeToLogs(log_str)
