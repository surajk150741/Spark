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

from pyspark.sql.functions import pandas_udf, PandasUDFType
import h3_pyspark

## oci imports
import oci
import os
import io
import sys
from pathlib import Path
from oci.config import validate_config
from oci.object_storage import ObjectStorageClient

#ociconf = oci.config.from_file()

spark = SparkSession.builder.appName("STEP01_h9filtered") \
        .config("spark.scheduler.mode", "FAIR") \
        .config("spark.delta.logStore.oci.impl","io.delta.storage.OracleCloudLogStore")\
        .config("spark.pyspark.virtualenv.enabled", "true") \
        .config("fs.oci.client.custom.authenticator", "com.oracle.bmc.hdfs.auth.InstancePrincipalsCustomAuthenticator")\
        .getOrCreate()
#       .config("spark.driver.memory", "56g") \
#        .config("spark.driver.cores", "4") \
#        .config("spark.executor.memory", "20g") \
#        .config("spark.executor.cores", "2") \
#        .config("spark.executor.instances", '76')\
#       .config("spark.default.parallelism", '120')\
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
source_date= "2022-07-09"#dbutils.widgets.get('source_date')#"2021-11-15"
country= "IND"#dbutils.widgets.get('country')#"USA"
source = "GRAVY"
#day_values = [dt.datetime.strftime(dt.datetime.strptime(source_date, "%Y-%m-%d")-dt.timedelta(x), "%Y-%m-%d") for x in range(0,14)]
paths= f"oci://ia-customer-insights@bmmp5bv7olp2/{source.lower()}_data/hdfs_data/step_0_filtered_h9/{country}/"
#f"oci://ia-customer-insights@bmmp5bv7olp2/{source.lower()}_data/hdfs_data/step_0/{country}/"
#f"oci://ia-customer-insights@bmmp5bv7olp2/{source.lower()}_data/hdfs_data/Updated_{source}/{country}/{source_date}"
is_delta =  True#if str(dbutils.widgets.get('is_delta')).lower() == "true" else False

today = (date.today()).strftime("yyyy-mm-dd")



# %%
##correcting day values if required 
#day_values.append("2022-02-25")


# %%
namespace = "bmmp5bv7olp2"


signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
identity_client = oci.identity.IdentityClient(config={}, signer=signer)
object_storage_client = ObjectStorageClient(signer=signer, config={})
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


from user_agents import parse 

day_values =[ (datetime.now()-timedelta(days = x)).strftime("%Y-%m-%d") for x in number_of_days]

for source_date in day_values:
    
    unique_token=f"PROD_API_STEP_01_{today}_{source_date}_{country}_{source}"

    print(paths)
    str_arg =""

    str_arg = ""
    tminus = dt.datetime.strptime(source_date, "%Y-%m-%d")#date.today() - timedelta(days=int(38))# 2021-04-12
    print(tminus)
    date_string = tminus.strftime('%d')
    month_string = tminus.strftime('%m')
    print(date_string)

    token = requestId = unique_token#"{}_{}".format(unique_token, source_date)
    
    def createLogs():
        global object_storage_client
        try:
            bucket_name = "ia-location-data"
            f = BytesIO()
            FILE_PATH = ""
            more_binary_data = str(f.getvalue().decode()) + "request_id="+requestId+";notebook_name=Date wise Split for Vendor data;start_time="+str(time.time())+"\n request_id="+requestId+";message=Started Date wise split \n"
        #analytics_logs = str(f.getvalue().decode()) +  str(text_string)
        # Method 1: Object.put()
            #validate_config(ociconf)
            bucket_name = "ia-mobility-logs"
            #object_storage_client = ObjectStorageClient(ociconf)
            logs_path = 'logs/{0}/{2}/{1}_date_split_h9filtered.txt'.format(str(tminus.strftime('%Y-%m-%d')), country, source)
            object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
        except Exception as e:
            print(e)
        
    createLogs()

    def writeToLogs(str_arg):
        try:
            f = BytesIO()
            bucket_name = "ia-mobility-logs"
            logs_path = 'logs/{0}/{2}/{1}_date_split_h9filtered.txt'.format(str(tminus.strftime('%Y-%m-%d')), country, source)
            #object_storage_client = ObjectStorageClient(ociconf)
            file_data = object_storage_client.get_object(namespace,bucket_name, logs_path)
            f.seek(0)
    
            more_binary_data =  str(file_data.data.text)+"\n"+"notebook_name=HDFS Ingest;" +  str(str_arg)
            #print(more_binary_data)
            object_storage_client.put_object(namespace, bucket_name, logs_path, put_object_body=more_binary_data)
            return "completed"
        except Exception as e:
            print(e)
            return e
        
    
    # Define our function that return according to UDF schema
    def parse_ua(ua_string):
        # parse library cannot parse None
        if ua_string is None:
            ua_string = ""

        parsed_string = parse(ua_string)

        output =  [
            parsed_string.device.brand,
            parsed_string.device.family,
            parsed_string.device.model,

            parsed_string.os.family,
            parsed_string.os.version_string,

            parsed_string.browser.family,
            parsed_string.browser.version_string,

            (parsed_string.is_mobile or parsed_string.is_tablet),
        parsed_string.is_bot
        ]
        # If any of the column have None value it doesn't comply with schema
        # and thus throw Null Pointer Exception
        for i in range(len(output)):
            if output[i] is None:
                output[i] = 'Unknown'
        return output
    
    # Our schema of parsing outcome
    ua_parser_udf = F.udf(lambda z: parse_ua(z), StructType([
            StructField("device_brand", StringType(), False),
            StructField("device_family", StringType(), False),
            StructField("device_model", StringType(), False),

            StructField("os_family", StringType(), False),
            StructField("os_version", StringType(), False),

            StructField("browser_family", StringType(), False),
            StructField("browser_version", StringType(), False),

            StructField("is_mobile", BooleanType(), False),
            StructField("is_bot", BooleanType(), False),
        ]))

    #   paths = "s3://ia-customer-insights/lf_data/hdfs_data/Updated_LS/{0}/{1}".format(country,source_date)
    print(paths)
    
    
    where_caluse = f'date = "{source_date}"'
    print(where_caluse)

    start_time = time.time()
    if is_delta == True:
        df = spark.read.format('delta').load(paths, header = 'true').where(where_caluse)
    else: 
        df = spark.read.format('parquet').load(paths, header = 'true').where(where_caluse)

    df = df.selectExpr('UUID', 'AAID as maid', "latitude", "longitude", "timestamp", "time_zone", "IP_address", "forensic_flag", "device_type","record_count", "country", "browser", "date")

    #people = spark.read..load(load_path)
    #df.show(5)
    log_str= "request_id="+requestId+";task_id=1.0;task_name=Read file from input;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)
    start_time = time.time()

    #df.select('country').distinct().show()

    # dftest = df_final.filter((df_final.state == 'UP') | (df_final.state == 'MP'))
    
    df0 = df.filter(df.country == country)
    numPartitions = 800
    dfPartitioned = df0#.repartition(numPartitions)
    log_str= "request_id="+requestId+";task_id=1.1;task_name=Repartition data;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)

    # to custom run for specific dates
    #dfPartitioned = dfPartitioned.filter((dfPartitioned.date == '2021-05-11'))

    df1 = dfPartitioned.filter(dfPartitioned.latitude != "0.0")# | (dfPartitioned.longitude != "0.0"))
    df1 = df1.filter(df1.longitude != "0.0")

    df1 = df1.withColumn("latitude",col("latitude").cast(DoubleType())) \
        .withColumn("longitude",col("longitude").cast(DoubleType()))

    #df2 = df1.withColumn("timestamp", df["timestamp"] / 1000)
    #df2 = df1.withColumn("timestamp", F.from_unixtime(F.col("timestamp"), 'yyyy-MM-dd HH:mm:ss').cast("timestamp"))
    # df2.show()
    #df3 = df1.withColumn('date', F.to_date(col('timestamp')).cast("date"))
    #df3.show(3)

    def return_index(lat, long):
        return [h3.geo_to_h3(float(lat), float(long), 9)]

    schema = StructType([
        StructField("h3", StringType(), False)
    ])


    loc_test = udf(lambda a,b: return_index(a,b), schema)

    start_time = time.time()
    #ifa_indexed = df1.select('maid', 'latitude','longitude', 'date','carrier','city_hasc','timestamp','postcode','user_agent', loc_test("latitude","longitude").alias('indexH3'))
    # ifa_indexed = df4.select('poi', 'lat','long', 'date', loc_test('lat','long').alias('indexH3'))
    #ifa_indexed_store = ifa_indexed.select("maid", "latitude", "longitude", "date", 'carrier','timestamp','postcode','city_hasc','user_agent','indexH3.h3')

    ##UDF based h9 creation
    #h3_func9 = lambda lat, lng: h3.geo_to_h3(float(lat), float(lng), resolution =9)
    #h3_full_function9 = F.udf(h3_func9)
    #ifa_indexed_store_1 = df1.withColumn("h3", h3_full_function9(*[F.col(x) for x in ["latitude", "longitude"]]))

    #h3_pyspark based udf creation
    df1 = df1.withColumn('9_index', lit(9))
    ifa_indexed_store_1 = df1.withColumn('h3', h3_pyspark.geo_to_h3('latitude','longitude', '9_index'))
    ifa_indexed_store = ifa_indexed_store_1.select("maid", "latitude", "longitude", "date",'timestamp','h3', 'forensic_flag')
    ifa_indexed_store.show(2)

    log_str= "request_id="+requestId+";task_id=2.0;task_name=Index data on h9 index;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)

    

    start_time = time.time()

    #polygon_data = spark.read.format('csv').load(polygon_data_path.split(','), header = 'true')
    #polygon_data = polygon_data.selectExpr("state as state", "city as p_city", "idx9 as h3")
    #polygon_data.show(3)
    log_str= "request_id="+requestId+";task_id=2.1;task_name=Load polygon data;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
             ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)

    data_union = ifa_indexed_store#.join(polygon_data, on=["h3"], how='inner')      #### **************
    #data_union.show(3)

    #data_union.show(3)

    # data_union.show(3)

    ##### hour of the day
    from pyspark.sql.functions import substring

    dfx1 = data_union.withColumn("time_precision_till_minutes", substring(col("timestamp"),0,16))
    #dfx1.show(3)
    print(dfx1.count())
    dfx2 = dfx1.dropDuplicates(["maid","h3","time_precision_till_minutes"])
    print(dfx2.count())
    dfx2 = dfx2.select(['maid', 'latitude', 'longitude', 'date','timestamp', 'forensic_flag', 'h3'])

    dfx2 = dfx2.selectExpr("maid as ifa","latitude as lat","longitude as long","date as date","timestamp as timestamp", "forensic_flag")

        
    
    #dfx2.show(5)

    indexing_level = 12
    partition_level = 6

    dfx2 = dfx2.withColumn('indexing_level', lit(indexing_level))\
        .withColumn('partition_level', lit(partition_level))


    def return_index(lat, long):
        return [h3.geo_to_h3(float(lat), float(long), 9), h3.geo_to_h3(float(lat), float(long), indexing_level), h3.geo_to_h3(float(lat), float(long), partition_level)]

    schema = StructType([
        StructField("h3", StringType(), False),
        StructField("h12", StringType(), False),
        StructField("h6", StringType(), False)
    ])

    loc_test = udf(lambda a,b: return_index(a,b), schema)

    start_time = time.time()

    #ifa_indexed = dfx2.select('ifa', 'lat','long', 'date','carrier','city','timestamp','zip','state','user_agent', loc_test("lat","long").alias('indexH3'))
    # ifa_indexed = df4.select('poi', 'lat','long', 'date', loc_test('lat','long').alias('indexH3'))
    #ifa_indexed_store = ifa_indexed.select("ifa", "lat", "long", "date", 'carrier','timestamp','zip','user_agent','city','state','indexH3.h3', 'indexH3.h12','indexH3.h6')

    ifa_indexed_store = dfx2.withColumn('h12', h3_pyspark.geo_to_h3('lat','long', 'indexing_level'))\
                               .withColumn('h6', h3_pyspark.geo_to_h3('lat','long', 'partition_level'))

    log_str= "request_id="+requestId+";task_id=2.2;task_name=Index data on h6 index;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
         ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)


    # tminus = date.today() - timedelta(days=2)
    # tminus_save = tminus.strftime("%B%d")
    # #tminus_save = "April17"
    # save_string = "s3://ia-customer-insights/lf_data/hdfs_data/lf/new_schema_with_agent/Updated_si_{}.parquet".format(tminus_save)
    # save_string

    cols1 = ["h6","h12"]

    dfx5 = ifa_indexed_store.orderBy(cols1)

    dfx5.columns
    start_time = time.time()
    '''
    df_final = dfx5.withColumn('parsed', ua_parser_udf('user_agent')) \
    .select('user_agent','ifa', 'lat', 'long', 'date', 'carrier', 'timestamp', 'zip', 'city', 'state', 'h3', 'h12', 'h6',
        F.col('parsed.device_brand').alias('device_brand'),
        F.col('parsed.device_family').alias('device_family'),
        F.col('parsed.device_model').alias('device_model'),
        F.col('parsed.os_family').alias('os_family'),
        F.col('parsed.os_version').alias('os_version'),

        F.col('parsed.browser_family').alias('browser_family'),
        )
    '''

    df_final = dfx5.select('ifa','date','timestamp','h12', 'h6','forensic_flag' )

    df_final = df_final.withColumn('country', lit(country))

    #df_final.show(5)

    log_str= "request_id="+requestId+";task_id=2.3;task_name=Parse user agent;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
             ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
    writeToLogs(log_str)

    #df_final.write.mode('overwrite').option("timestampFormat", "yyyy-MM-dd HH:mm:ss").format("csv").save(save_string , header = True)

    # df_final.write.parquet(save_string)


    """# Save output"""

    # country, date_string1, month_string1

    # folder_date = f"2021-{month_string1}-{date_string1}"
    folder_date = source_date
    #folder_date

    save_string = f"oci://ia-customer-insights@bmmp5bv7olp2/lf_data/hdfs_data/{source.lower()}/delta/step_1_alt_h9altered/"
    #save_string

    # dftest = df_final.filter((df_final.state == 'UP') | (df_final.state == 'MP'))
    # dftest = df_final.filter((df_final.state == 'DL'))
    # dftest = dftest.withColumn('district', F.split(dftest['city'], '\.').getItem(2))

    # dftest.show(6)

    # df_final = df_final.withColumn('district', F.split(df_final['city'], '\.').getItem(2))



    # for f in *; do mv $f ${f/${f:0:5}/} ; done

    # aws s3 --recursive mv s3://<bucketname>/<folder_name_from> s3://<bucket>/<folder_name_to>

    """# TEST"""

    # an = spark.read.parquet("s3://ia-customer-insights/lf_data/hdfs_data/ls/IND/2021-05-15/state=DL/district=CD/h3=863da1147ffffff/*.parquet")

    # an.show(7)

    # an.select("city").distinct().count()

    #
    df_final_write = df_final
    #df_final_write.show(3)
    df_final_write = df_final_write.withColumn('h12_int', h3_pyspark.string_to_h3('h12'))
    df_final_write = df_final_write.withColumn('h6_int', h3_pyspark.string_to_h3('h6'))

    #df_final_write_h6 = df_final_write.select(df_final_write.h6).distinct()
    #df_final_write_h6.count()
    #df_final_write_h6_count = df_final_write.groupBy(df_final_write.h6).count()
    #df_final_write_h6_count.orderBy(desc('count'))
    #display(df_final_write_h6_count)
    #print(df.count())
    #print(df_final_write.filter(col('date')=="2022-03-01").count())
    df_final_write.show(3)

    df_final_write = df_final_write.withColumn("forensic_flag_bin", bin(col("forensic_flag")))
    df_final_write.orderBy(col("forensic_flag_bin").desc())#.show(10)
    accuracy_map = {
        "001":"High_0_35", 
        "000" : "No_accuracy",
        "010" : "Moderate_50_220",    
        "011" :  "Moderate_high_35_50",
        "100" :   "Low_250_1000" ,
        "110" :  "Moderate_low_220_250", 
        "1": "High_0_35", 
        "11":  "Moderate_high_35_50",
        "10": "Moderate_50_220",
        "": "flag_unavailable"
               }

    df_final_write = df_final_write.withColumn("forensic_flag_bin", col("forensic_flag_bin").cast(StringType()))\
                    .withColumn("forensic_flag_bin", lpad(col("forensic_flag_bin"), 28,'0'))

    df_final_write = df_final_write.withColumn("accuracy_bin", col("forensic_flag_bin").substr(11,3))

    df_final_write.show(3)
    
    df_final_write = df_final_write.withColumn("accuracy", when(col("accuracy_bin") == "000", "no_accuracy")
                                           .when(col("accuracy_bin") == "001", "High_0_35")
                                           .when(col("accuracy_bin") == "010", "Moderate_50_220")
                                           .when(col("accuracy_bin") == "011", "Moderate_high_35_50")
                                           .when(col("accuracy_bin") == "100", "Low_250_1000")
                                           .when(col("accuracy_bin") == "110", "Moderate_low_220_250")
                                           .when(col("accuracy_bin") == "1", "High_0_35")
                                           .when(col("accuracy_bin") == "11", "Moderate_high_35_50")
                                           .when(col("accuracy_bin") == "10", "Moderate_50_220")
                                           .when(col("accuracy_bin") == "", "flag_unavailable")
                                           .otherwise("flag_unavailable")
                                                           )

    df_final_write.show(3)
    
    #verify the accuracy count
    #accuracy_count = df_final_write.groupBy("accuracy").count()
    #print(accuracy_count.show(20))
    df_to_write = df_final_write.select('ifa','date', 'country', 'h6', 'h12', 'timestamp', 'accuracy', 'h6_int', 'h12_int')

    df_to_write.show(3)
    
    start_time = time.time()
    try:
        #df_final.write.partitionBy(["date", "state", 'city', 'h3']).mode("append").format('parquet').save(save_string)
        df_final_write.orderBy(["date", "h6", "h12"]) \
        .write \
        .partitionBy(["country","date"]) \
        .mode("append") \
        .format('delta') \
        .option("overwriteSchema", "true")\
        .save(save_string) 
        log_str= "request_id="+requestId+";task_id=3.0;task_name=Write to S3;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
             ";task_time_taken="+str(time.time()-start_time)+";status=suceessful;message=ok" 
        writeToLogs(log_str)
    except Exception as e:
        log_str= "request_id="+requestId+";task_id=3.0;task_name=Index data on h9 index;task_start_time="+str(start_time)+";task_end_time="+str(time.time())+\
             ";task_time_taken="+str(time.time()-start_time)+";status=error;message=fail;error_message="+str(e) 
        writeToLogs(log_str)
        print(e)

    writeToLogs(f"Final process completed for {len(source_date)} number of days")
    

# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%
'''df_final_write = dfx5.withColumn('parsed', ua_parser_udf('user_agent')) \
.select('user_agent','ifa', 'lat', 'long', 'date', 'carrier', 'timestamp', 'zip', 'city', 'state', 'h3', 'h12', 'h6',
        F.col('parsed.device_brand').alias('device_brand'),
        F.col('parsed.device_family').alias('device_family'),
        F.col('parsed.device_model').alias('device_model'),
        F.col('parsed.os_family').alias('os_family'),
        F.col('parsed.os_version').alias('os_version'),

        F.col('parsed.browser_family').alias('browser_family'),
        )
 '''

# %%
'''
ifa_count = df_final_write.groupby(["ifa", "state"]).count()

#unique_device_group = df_final_write.groupby(["ifa", "os_family"]).count()

device_group = df_final_write.groupby(["os_family"]).count()

unique_ifa_counts = df_final_write.groupby(["ifa"]).count()

# ifa_count.show(5)

state_count = df_final_write.groupby("state").count()

# state_count.show(5)

log_path = "s3://ia-mobility-logs/analytics/LS/{}/{}".format(folder_date, country)
log_path

try:
    ifa_count.write.partitionBy(["state"]).mode("append").format('parquet').save(log_path)
except Exception as e:
    str_arg = str_arg + "state wise split failed \n"+ str(e)
    writeToLogs(str_arg)



state_path = "s3://ia-mobility-logs/analytics/LS/{0}/{1}_state_count.csv".format(folder_date, country)

device_type_path = "s3://ia-mobility-logs/analytics/LS/{1}/{0}_device_OS_count.csv".format(unique_token,folder_date)


ifa_pings_path = "s3://ia-mobility-logs/analytics/LS/{1}/{0}_ifa_pings_count.csv".format(unique_token,folder_date)
print(state_path)
'''

# %%
'''
try:
    state_count.coalesce(1).write.mode("append").format("csv").option("header", "true").save(state_path)
except Exception as e:
    str_arg = str_arg + "Count by state failed \n"
    writeToLogs(str_arg)
    
try:
    device_group.coalesce(1).write.mode("append").format("csv").option("header", "true").save(device_type_path)
except Exception as e:
    str_arg = str_arg + "Count by Device OS failed \n"
    writeToLogs(str_arg)

try:
    unique_ifa_counts.coalesce(1).write.mode("append").format("csv").option("header", "true").save(ifa_pings_path)
except Exception as e:
    str_arg = str_arg + "Count by Device OS failed \n"
    writeToLogs(str_arg)
'''

# %%
spark.stop()

# %%



