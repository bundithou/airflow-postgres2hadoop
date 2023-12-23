from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
import time
# the Spark session should be instantiated as follows
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.master", "spark://spark-master:7077") \
    .config("spark.sql.parquet.writeLegacyFormat", True)\
    .getOrCreate()

# read raw data
df = spark.read.parquet("hdfs://namenode:8020/user/spark/order_detail")
raw_columns = df.columns
print(f"raw columns: {raw_columns}")
print(f"raw column count: {len(raw_columns)}")
df.printSchema()

# standardize
df = df.withColumn('discount_no_null', F.col('discount'))
df = df.na.fill({'discount_no_null':0.0})

row_cnt = df.count()
print(f"row count: {row_cnt}")
new_columns = df.columns
print(f"raw columns: {new_columns}")
print(f"raw column count: {len(new_columns)}")
df.printSchema()

# write
df.write.parquet('hdfs://namenode:8020/user/spark/order_detail_new', partitionBy='dt', mode='overwrite')
# df.persist()
# for m in range(12):
#     df.filter(F.month('order_created_timestamp') == F.lit(m+1)).write.parquet('hdfs://namenode:8020/user/spark/order_detail_new', partitionBy='dt', mode='overwrite')
#     time.sleep(3)
spark.stop()
