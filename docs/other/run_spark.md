
```bash
docker container exec -it docker-spark-master-1 sh
```

```bash
spark-submit --driver-class-path script/jars/postgresql-42.7.0.jar --name test script/src/test.py  
spark-submit --name test2 /usr/local/spark/src/transform_order_detail_v2.py

spark-submit --name test2 /usr/local/spark/src/aggregate_v2.py
```
