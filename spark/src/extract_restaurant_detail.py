from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T

# the Spark session should be instantiated as follows
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "/usr/local/spark/jars/postgresql-42.7.0.jar") \
    .config("spark.master", "spark://spark-master:7077") \
    .config("spark.sql.parquet.writeLegacyFormat", True)\
    .getOrCreate()

df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/airflow")\
    .option("dbtable", "restaurant_detail") \
    .option("user", "airflow") \
    .option("password", "airflow") \
    .option("driver", "org.postgresql.Driver") \
    .load()

row_cnt = df.count()
print(f"row count: {row_cnt}")

# jdbcDF.printSchema()
# df = df.withColumn('order_created_timestamp', F.to_timestamp('order_created_timestamp'))
df = df.withColumn('estimated_cooking_time', F.col('estimated_cooking_time').cast(T.FloatType()))
df = df.withColumn('latitude', F.col('latitude').cast(T.DecimalType(11,8)))
df = df.withColumn('longitude', F.col('longitude').cast(T.DecimalType(11,8)))
df = df.withColumn('dt', F.lit("latest"))
df.write.parquet('hdfs://namenode:8020/user/spark/restaurant_detail', partitionBy='dt', mode='overwrite')

spark.stop()
