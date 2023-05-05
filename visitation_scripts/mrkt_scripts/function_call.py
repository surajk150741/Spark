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

spark = SparkSession.builder.appName("step4analysis") \
        .config("spark.driver.memory", "40g") \
        .config("spark.driver.cores", "8") \
        .config("spark.executor.memory", "9g") \
        .config("spark.executor.cores", "5") \
        .config("spark.scheduler.mode", "FAIR") \
        .config("spark.executor.instances", '23')\
        .config("spark.default.parallelism", '228')\
        .config("spark.delta.logStore.oci.impl","io.delta.storage.OracleCloudLogStore")\
        .config("fs.oci.client.custom.authenticator", "com.oracle.bmc.hdfs.auth.InstancePrincipalsCustomAuthenticator")\
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

from parameters import *

from all_functions import *


start_date = "2023-03-19"
end_date = "2023-03-24"
#token = f"{start_date}_{end_date}_correct"
token = f"{start_date}_{end_date}"
clients = ['jbcn']     #,'jcb']#,'ciplaII']#,'cipla','lyef','daybreak','osg','bajaj','scaler','shemaroo'

## INPUT FROM all_functions.py module
inputs = inputs()
poi = inputs.poi
visits = inputs.visits

for client in clients:
    if client == 'jbcn':
        
        #for google category
        for i in range(len(jbcn_cases_list)):
            dfv = poi_district_visits(jbcn_poitype_list[i],jbcn_city_list,start_date,end_date)
            dfp = google_data(poi, jbcn_cases_list[i])
            df_final, x1 = join_data(dfv, dfp) 
            write_data(df_final,client, jbcn_cases[i], jbcn_city_name, token, x1)
        
        #for brand
        dfvb = poi_district_visits(jbcn_poitype_brand,jbcn_city_list,start_date,end_date)
        dfpb = brand_data(poi, jbcn_poitype_brand)
        df_final_b, x2 = join_data(dfvb, dfpb) 
        write_data(df_final_b,client, 'brands_of_arcade_cinema', jbcn_city_name, token, x2)   #### can i write something like this?
        
        #for names
        dfvn = poi_district_visits(jbcn_poitype_brand,jbcn_city_list,start_date,end_date)
        dfpn = name_data(poi, jbcn_names)
        dfjoin = join_data(dfvb, dfpb) 
        for q in jbcn_wbi_cases:
            df1 = wbi_data(client,q,token)
            dfjoin = join_data(dfjoin,df1)
        dffinal, xw = count_data(dfjoin)


        write_data(dffinal, client, 'target_socities', 'new_requirement', token, xw)   #### can i write something like this?
        
        #rest poitypes
        dfr = poi_district_visits(jbcn_poitype_rest,jbcn_city_list,start_date,end_date)
        dffr, x3 = count_data(dfr)
        write_data(dffr, client, 'rest', jbcn_city_name, token, x3)
'''
    elif client == 'jcb':
        
        #normal visits
        for i in range(len(jcb_poitype_list)):
            df1 = visits_only_data(jcb_poitype_list[i],jcb_city_list,start_date,end_date)
            dff2, x1 = count_data(df1)
            write_data(dff2,client, jcb_cases[i], jcb_city_name, token, x1)
        
        #for brand
        dfvb = visits_only_data(jcb_poitype_brand,jcb_city_list,start_date,end_date)
        dfpb = brand_data(poi_data(), jcb_poitype_brand)
        df_final_b, x2 = join_data(dfvb, dfpb) 
        write_data(df_final_b,client, 'for_brands_of_beauty_hair', jcb_city_name, token, x2)   #### can i write something like this?
        
    elif client == 'ciplaII':
        # normal visits are remaining
        for i in range(len(cipla_poitype_list)):
            df1 = visits_only_data(cipla_poitype_list[i],cipla_city_list,start_date,end_date)
            dff2, x1 = count_data(df1)
            write_data(dff2,client, cipla_cases[i], cipla_city_name, token, x1)
''' 
'''  
#for source_client_name
dfvb = visits_only_data(['building.residential.apartment'],['IN.MH.PU','IN.TN.CO'],start_date,end_date)
dfpb = source_data(poi_data(), ['IA_Adonmo'])
df_final_b, x2 = join_data(dfvb, dfpb) 
write_data(df_final_b,client, 'daily_travel_commute_adonmo', 'pune_coimbatore', token, x2)   #### can i write something like this?
'''
        
