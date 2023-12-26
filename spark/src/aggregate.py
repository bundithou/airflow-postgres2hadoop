from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T

# the Spark session should be instantiated as follows
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.master", "spark://spark-master:7077") \
    .config("spark.sql.parquet.writeLegacyFormat", True)\
    .getOrCreate()

# read raw data
order = spark.read.parquet("hdfs://namenode:8020/user/spark/order_detail_new")
restaurant = spark.read.parquet("hdfs://namenode:8020/user/spark/restaurant_detail_new")

# joinned by restaurant id
df = order.join(restaurant, on = order.restaurant_id == restaurant.id, how='left')

# Get the average discount for each category
avg_discount_cat = df.groupby('category').avg('discount', 'discount_no_null')
avg_discount_cat.show()

# Row count per each cooking_bin
cnt_cooking_bin = df.groupby('cooking_bin').count()
cnt_cooking_bin.show()

avg_discount_cat.coalesce(1).write.csv('/opt/bitnami/spark/sql_result/discount', header=True, mode='overwrite')
cnt_cooking_bin.coalesce(1).write.csv('/opt/bitnami/spark/sql_result/cooking', header=True, mode='overwrite')

