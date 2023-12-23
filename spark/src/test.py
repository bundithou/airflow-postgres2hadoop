from pyspark.sql import SparkSession

# the Spark session should be instantiated as follows
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "/usr/local/spark/jars/postgresql-42.7.0.jar") \
    .config("spark.master", "spark://spark-master:7077") \
    .getOrCreate()

jdbcDF = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/airflow")\
    .option("dbtable", "order_detail") \
    .option("user", "airflow") \
    .option("password", "airflow") \
    .option("driver", "org.postgresql.Driver") \
    .load()

row_cnt = jdbcDF.count()
print(f"row count: {row_cnt}")

jdbcDF.printSchema()