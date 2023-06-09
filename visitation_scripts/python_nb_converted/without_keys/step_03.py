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

spark = SparkSession.builder.appName("step_03") \
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

# %%
##Arguments##

country= "IND"#dbutils.widgets.get('country')#"USA"
poi_type = ""
district_code = ""
client = "all_ind_3.4_all"
indexing_level = 12
source = "GRAVY"
today = (date.today()).strftime("yyyy-mm-dd")
token = f"test_poi_pipeline_{country}_{today}_{client}"
version = ""
poi_version = '3.4'
print(poi_type)


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

namespace = "bmmp5bv7olp2"
signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
identity_client = oci.identity.IdentityClient(config={}, signer=signer)
today = datetime.today().strftime('%Y-%m-%d')
     

def createLogs():
    try:
        f = BytesIO()

        bucket_name = "ia-mobility-logs"
        more_binary_data = str(f.getvalue().decode()) + "request_id="+token+";notebook_name=poi processing;start_time="+str(time.time())+"\n request_id="+token+";message=poi processing \n"
        #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
        # Method 1: Object.put()
        #validate_config(ociconf)
        logs_path = f"logs/{client}/{today}_{hash_poi}_new_mobility_step_03.txt"
        object_storage_client = ObjectStorageClient(signer=signer, config={})
        
        object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
    except Exception as e:
        print(e)

createLogs()

def writeToLogs(str_arg):
    try:
        f = BytesIO()
        bucket_name = "ia-mobility-logs"
        logs_path = f"logs/{client}/{today}_{hash_poi}_new_mobility_step_03.txt"
        object_storage_client = ObjectStorageClient(signer=signer, config={})
        file_data = object_storage_client.get_object(namespace,bucket_name, logs_path)
        
        more_binary_data = str(file_data.data.text)+"\n"+"notebook_name=poi processing;" + str(str_arg)
        #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
        # Method 1: Object.put()
        object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
        return "completed"
        
    except Exception as e:
        print(e)
        return e


# %%
def getPath(country):
    if "road" in client:
        print('yes')
        paths = {
            "USA": "s3://ia-customer-insights/poi_data/all_POI_updated_parquet_data/country=USA/*/*.parquet",
            "ARE": "s3://ia-customer-insights/poi_data/ARE_second_compressed_parquet_data/",
            "IND": "s3://ia-customer-insights/poi_data/all_POI_updated_parquet_data_road/country=IND/*/*.parquet"
        }
    else: 
        print('no')
        paths = {
            "USA": "oci://ia-visitation-data@bmmp5bv7olp2/poi_data/delta/all_POI_updated_incremental_data/",
            "ARE": "s3://ia-customer-insights/poi_data/ARE_second_compressed_parquet_data/",
            "IND": f"oci://ia-visitation-data@bmmp5bv7olp2/poi_data/delta/all_POI_updated_incremental_data_{poi_version}/"
        }
    return paths[country]
#IND "s3://ia-customer-insights/poi_data/all_IND_complete_compressed_parquet_data/*/*/*.parquet"
#"IND": "s3://ia-customer-insights/poi_data/IND_here_compressed_parquet_data/*.parquet"
#ARE : "s3://ia-customer-insights/poi_data/all_pois_final_ARE/*.parquet",
#"IND": "s3://ia-customer-insights/poi_data/all_pois_final_IND/*.parquet"
#block_path = "s3://ia-customer-insights/poi_data/USA_compressed_parquet_data/*.parquet"#add the h12 POIs path
start_time = time.time()
block_path = getPath(country)
print(block_path)
#log_str= "request_id="+token+";task_id=1.0;task_name=Get POI path;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
#         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
#print(writeToLogs(log_str))

# %%
try:
    create_poi_hash = True
    start_time = time.time()
    save_string = f"oci://ia-customer-insights@bmmp5bv7olp2/poitype_list/delta/step_03_alt/{str(hash_poi)}/" #"s3://ia-customer-insights/poitype_list/delta/"+ country + "/" +client+"/"+str(hash_poi)   
    df_poi = spark.read.format("delta").load(save_string.split(','),header = True)
    df_poi.show(2)  
    print("in try POI ....")
    print(save_string)
    log_str= "request_id="+token+";task_id=1.1;task_name=Read file from Existing hash of POI;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    print(writeToLogs(log_str))
    
except Exception as e:
    create_poi_hash = True
    print("exception")

# %%
if(create_poi_hash):
    start_time = time.time()
    ##### POI intersection #######
    print("from database...")
    
    df_poi = spark.read.format("delta").load(block_path, header = 'true').where(f"country = '{country}'")
    df_poi.show(3)
    print(save_string)
    
    log_str= "request_id="+token+";task_id=1.2;task_name=Read POI data from delta;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    print(writeToLogs(log_str))
    

# %%
if(create_poi_hash):
    if(poi_type != ""):
        start_time = time.time()
        poi_type_filter = f"poiType in ({poi_type})"
        print("poitype_filter",poi_type_filter )
        df_poi = df_poi.filter(df_poi.poiType.isin(poi_type_list))
        log_str= "request_id="+token+";task_id=1.3;task_name=Filter POI data for selected POITypes;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok"
        print(writeToLogs(log_str))
    
    df_poi = df_poi.filter(df_poi.resolution >= indexing_level)
    df_poi.show(3)
    
    start_time = time.time()
    
    def h9_filter(hindex):
      try:
        return [h3.h3_to_parent(hindex, indexing_level)]
      except Exception as error:
        return ["0"]
    
    schema = StructType([
        StructField("hindex", StringType(), False)
    ])

    h9_filter_speedup = udf(lambda a: h9_filter(a), schema)
    
    if(district_code != ""):
        df_poi = df_poi.filter(col('p_city').isin(district_code_list))
        print(df_poi.count())
    
        
    ## from database conversion for h12
    print(indexing_level)
    if(indexing_level != 12):
        df_poi = df_poi.withColumn('indexing_level', lit(indexing_level))
        df_poi = df_poi.withColumn('h3index', h3_pyspark.h3_to_parent('h3index', 'indexing_level'))
        #df_poi = df_poi.select('poiCode', 'poiType', 'h3index', h9_filter_speedup('h3index').alias('H3'))
        #df_poi = df_poi.select('poiCode', 'poiType','H3.hindex')
        #df_poi = df_poi.withColumnRenamed("hindex","h3index")
        log_str= "request_id="+token+";task_id=1.4;task_name=Indexing filter modification;task_start_time="+str(start_time)+";\task_end_time="+str(time.time())+";\
        task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
        print(writeToLogs(log_str))
    # df_poi.show(3)    
    #### from database conversion for h12
    
        df_poi =df_poi.selectExpr("poicode as poiCode","poiType as poiType","h3index as h3")    
#     df_poi.show(3)
    #df_poi
    

# %%
if(create_poi_hash):
    df_poi.show(3)
    df_poi = df_poi.withColumn('h6_int', h3_pyspark.string_to_h3('h6')) \
                   .withColumn('h12_int', h3_pyspark.string_to_h3('h12')) \
                   .withColumn('h9_int', h3_pyspark.string_to_h3('h3')) \
                   .withColumn('country', lit(country)) \
                   .withColumnRenamed('p_city', 'district_code')
    
    df_poi.show(3)

# %%
if(create_poi_hash):  
    start_time = time.time()
    save_string = f"oci://ia-visitation-data@bmmp5bv7olp2/poitype_list/delta/step_03_alt/{str(hash_poi)}/" 
    print(save_string)
    
    df_poi.show(3)
    
    df_poi = df_poi.withColumn("version", lit("3.1.6_buffered"))
    
    df_poi.write.partitionBy(["version","country", "district_code"]).format("delta").mode('append').option("timestampFormat", "yyyy-MM-dd HH:mm:ss").save(save_string,header =True)
    
    log_str= "request_id="+token+";task_id=1.3;task_name=Write file to hash format for future use;\
    task_start_time="+str(start_time)+";task_end_time="+str(time.time())+";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    print(writeToLogs(log_str))

    save_string = f"oci://ia-visitation-data@bmmp5bv7olp2/poitype_list/delta/step_03_alt/{str(hash_poi)}/"   
    df_poi = spark.read.format("delta").load(save_string.split(','),header = True)
    df_poi.show(2)

# %%
spark.stop()


