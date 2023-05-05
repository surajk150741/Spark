# -*- coding: utf-8 -*-
"""ETL_Mobility_Step_02(1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zPUbG2h9mmZeWDe1a0UMUQlTfsv1Q9MM
"""

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

#
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


import h3_pyspark
#spark.sql.autoBroadcastJoinThreshold = -1

## oci imports
import oci
import os
import io
import sys
from pathlib import Path
from oci.config import validate_config
from oci.object_storage import ObjectStorageClient

#ociconf = oci.config.from_file()


spark = SparkSession.builder.appName("step_02") \
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

##Arguments##
source_date = sys.argv[1]#"2022-10-01"#dbutils.widgets.get('source_date') #"2021-11-15"
country = sys.argv[2]#"USA"#dbutils.widgets.get('country')#"USA"
is_delta = True#sys.argv[3] #if str(dbutils.widgets.get('is_delta')).lower() == "true" else False 
source = "GRAVY"#dbutils.widgets.get('source')#"ls"
today = (date.today()).strftime("yyyy-mm-dd")
version = ""
poi_version = '3.4.2'

print("source_date",source_date)
#"s3://ia-customer-insights/lf_data/hdfs_data/Updated_LS/ARE/"+source_date+"/" 


unique_token=f"PROD_API_{today}_{source_date}_{country}"

def getPath():
    if country == 'IND':
        path = f"oci://ia-visitation-data@bmmp5bv7olp2/poi_data/delta/unique_h12s_nonincremented_{poi_version}_all/"
    else:
        path = "oci://ia-visitation-data@bmmp5bv7olp2/poi_data/delta/unique_h12s_nonincremented_usa_3.1.2/"
    return path

block_path = getPath()


str_arg =""

str_arg = ""
tminus = dt.datetime.strptime(source_date, "%Y-%m-%d")#date.today() - timedelta(days=int(38))# 2021-04-12
print(tminus)
date_string = tminus.strftime('%d')
month_string = tminus.strftime('%m')
print(date_string)

token = requestId = "{}_{}".format(unique_token, source_date)

#spark = SparkSession.builder.config("spark.pyspark.virtualenv.enabled","true").getOrCreate()
#spark.conf.set("spark.sql.autoBroadcastJoinThreshold","5g")

namespace = "bmmp5bv7olp2"

signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
identity_client = oci.identity.IdentityClient(config={}, signer=signer)
#today = datetime.today().strftime('%Y-%m-%d')
def createLogs():

    try:
        bucket_name = "ia-mobility-logs"
        f = BytesIO()
        FILE_PATH = ""
        more_binary_data = str(f.getvalue().decode()) + "request_id="+requestId+";notebook_name=H9 based filtering;start_time="+str(time.time())+"\n request_id="+requestId+";message=Started Date wise split \n"
    #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
    # Method 1: Object.put()
        #validate_config(ociconf)
        bucket_name = "ia-mobility-logs"
        object_storage_client = ObjectStorageClient(signer=signer, config={})
        logs_path = 'logs/{0}/{2}/{3}_{1}_data_aggregator.txt'.format(source_date, country, source, today)
        object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
    except Exception as e:
        print(e)
    
createLogs()
def writeToLogs(str_arg):
    try:
        f = BytesIO()
        bucket_name = "ia-mobility-logs"
        logs_path = 'logs/{0}/{2}/{3}_{1}_data_aggregator.txt'.format(source_date, country, source,today)
        object_storage_client = ObjectStorageClient(signer=signer, config={})
        file_data = object_storage_client.get_object(namespace,bucket_name, logs_path)
        f.seek(0)

        more_binary_data =  str(file_data.data.text)+"\n"+"notebook_name=H9 based filtering;" +  str(str_arg)
        #print(more_binary_data)
        #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
        # Method 1: Object.put()
        #logs_path = 'logs/{0}/{1}_pre-process.txt'.format(str(tminus.strftime('%Y-%m-%d')), country)
        object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
        return "completed"
    except Exception as e:
        print(e)
        return e

start_time = time.time()

if is_delta == True:
    print('yes')
    paths = f"oci://ia-visitation-data@bmmp5bv7olp2/lf_data/hdfs_data/{source.lower()}/parquet/step_1_new/"
    #paths= f"oci://ia-visitation-data@bmmp5bv7olp2/lf_data/hdfs_data/{source.lower()}/delta/step_1/" 
    #"oci://ia-location-data@bmmp5bv7olp2/IND/delta/step_1_alt"
    #f"oci://ia-lifesight@bmmp5bv7olp2/lf_data/hdfs_data/{source}/delta/step_1_alt/"
    #"s3://ia-customer-insights/lf_data/hdfs_data/ls/delta/{0}/date={1}".format(country, source_date)
    df = spark.read.format('parquet').load(paths, header = 'true').filter(f"country == '{country}' and date == '{source_date}'")
else:
    print('no')
    
    paths= "oci://ia-visitation-data@bmmp5bv7olp2/lf_data/hdfs_data/ls/{0}/date={1}".format(country, source_date)
    df = spark.read.format('parquet').load(paths, header = 'true')
    
    df3 = df.withColumn("country", lit(country)).withColumn("converted_ts", when(col("country") == 'ARE', from_utc_timestamp(col("timestamp"), "Asia/Dubai")).otherwise(when(col("country") == 'IND', from_utc_timestamp(col("timestamp"), "Asia/Kolkata")).otherwise(from_utc_timestamp(col("timestamp"), "UTC"))))

    df = df3.withColumn('date', F.to_date(col('timestamp')).cast("date"))
    
    df = df.withColumn('index_res', lit(6))
    df = df.withColumn('h6', h3_pyspark.h3_to_parent('h3', 'index_res'))
    
    df = df.withColumn('resolution', lit(12))
    df = df.withColumn('h12', h3_pyspark.geo_to_h3('lat', 'long', 'resolution'))
    
df = df.dropDuplicates()
#people = spark.read..load(load_path)
#df.show(5)
#df.deleteDuplicates()
#dfc = df.count()
#print("dfc", dfc)
log_str= "request_id="+requestId+";task_id=1.0;task_name=Read file from input;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
writeToLogs(log_str)

#read h12 poi data
if(version != ""):
    print('yes')
    block_df = spark.read.format("delta")\
    .load(block_path, header = True) \
    .filter((col('country') == country) & (col('version') == version)) \
    .select("h12_int", "district_code","version")
else:
    print('no')
    block_df = spark.read.format("delta")\
    .load(block_path, header = True) \
    .filter(col('country')==country) \
    .select("h12_int", "district_code","version")
    
#block_df.show(3)

# join POI table and mobility data and remove all the h12 which don't have POIs
#set spark.sql.autoBroadcastJoinThreshold=-1
#if country != "USA":
#    data_union = df.join(broadcast(block_df), df.h12_int == block_df.h12_int) \
#                .select(df.h12, df.h6,df.h12_int, 
#                 df.h6_int,df.ifa, df.date, df.timestamp,df.country,block_df.district_code,block_df.version)
#else:
data_union = df.join(block_df, how = 'inner', on =["h12_int"]) \
                .select(df.h12, df.h6,df.h12_int, 
                 df.h6_int,df.ifa, df.date, df.timestamp,df.country,block_df.district_code,block_df.version)
#data_union.show(3)

data_union = data_union.orderBy(asc('district_code'), asc('h6_int'))
#data_union.show(3)

save_string = f"oci://ia-visitation-data@bmmp5bv7olp2/silver_level_first/daily_data/delta/step_2_v3.4/{source.lower()}/"
print(save_string)
#duc = data_union.count()
#print("data_union", duc)
data_union = data_union.withColumn("year", data_union.date.substr(1,4))


start_time = time.time()
try:
    data_union.write.partitionBy(['country','year','date','district_code']).mode("append").option("mergeSchema", "true").format('delta').save(save_string)
    log_str= "request_id="+requestId+";task_id=2.1;task_name=Write to S3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)
except Exception as e:
    log_str= "request_id="+requestId+";task_id=2.1;task_name=Write to s3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=fail;message=error;error_message="+str(e) 
    writeToLogs(log_str)
    print(e)

print("Completed the job")

spark.stop()
