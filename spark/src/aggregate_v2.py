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
order = spark.read.parquet("hdfs://namenode:8020/user/spark/transform_v2/order_detail_new")
restaurant = spark.read.parquet("hdfs://namenode:8020/user/spark/restaurant_detail_new")

# joinned by order id
df = order.join(restaurant, on = order.restaurant_id == restaurant.id, how='left')

# Get the average discount for each category
avg_discount_cat = df.groupby('category').avg('discount', 'discount_no_null')
avg_discount_cat.show()

# Row count per each cooking_bin
cnt_cooking_bin = df.groupby('cooking_bin').count()
cnt_cooking_bin.show()

# with open('file:///opt/bitnami/spark/sql_result/avg_discount_cat.csv', 'w') as f:
avg_discount_cat.coalesce(1).write.csv('/opt/bitnami/spark/sql_result/avg_discount_cat', header=True, mode='overwrite')

# with open('file:///opt/bitnami/spark/sql_result/cnt_cooking_bin.csv', 'w') as f:
cnt_cooking_bin.coalesce(1).write.csv('/opt/bitnami/spark/sql_result/cnt_cooking_bin', header=True, mode='overwrite')

