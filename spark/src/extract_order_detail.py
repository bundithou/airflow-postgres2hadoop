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
    .option("dbtable", "order_detail") \
    .option("user", "airflow") \
    .option("password", "airflow") \
    .option("driver", "org.postgresql.Driver") \
    .load()

row_cnt = df.count()
print(f"row count: {row_cnt}")

# jdbcDF.printSchema()
# df = df.withColumn('order_created_timestamp', F.to_timestamp('order_created_timestamp'))
df = df.withColumn('dt', F.date_format('order_created_timestamp', "yyyyMMdd").cast(T.StringType()))
# df = df.withColumn('price', F.col('price').cast(T.IntegerType()))
df = df.withColumn('discount', F.col('discount').cast(T.FloatType()))

df.printSchema()
df.write.parquet('hdfs://namenode:8020/user/spark/order_detail', partitionBy='dt', mode='overwrite')

spark.stop()
