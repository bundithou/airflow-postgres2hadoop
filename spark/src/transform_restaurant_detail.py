from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
# from pyspark.sql.functions import udf 
# from pyspark.sql.types import StringType, FloatType 
# the Spark session should be instantiated as follows
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.master", "spark://spark-master:7077") \
    .config("spark.sql.parquet.writeLegacyFormat", True)\
    .getOrCreate()

# Define a Python function to calculate the cooking_bin
def grading(number): 

    if number > 120: 
        # if greater than 120
        return 4

    elif number > 80:
        # 81-120
        return 3

    elif number > 40:
        # 41-80
        return 2

    elif number > 10:
        # 10-40
        return 1
    else:
        # otherwise
        return 0

calculate_cooking_bin = F.udf(lambda n: grading(n), T.IntegerType())

# read raw data
df = spark.read.parquet("hdfs://namenode:8020/user/spark/restaurant_detail")
raw_columns = df.columns
print(f"raw columns: {raw_columns}")
print(f"raw column count: {len(raw_columns)}")

# generate a new column
df = df.withColumn("cooking_bin", calculate_cooking_bin('estimated_cooking_time'))

row_cnt = df.count()
print(f"row count: {row_cnt}")
new_columns = df.columns
print(f"raw columns: {new_columns}")
print(f"raw column count: {len(new_columns)}")
df.show(5)

# write
df.write.parquet('hdfs://namenode:8020/user/spark/restaurant_detail_new', partitionBy='dt', mode='overwrite')
spark.stop()