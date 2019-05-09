from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType
import psycopg2
from datetime import datetime


fileschema = StructType().add("column1", StringType(), True)


def insert_record(record):
    try:
        connection = psycopg2.connect(
        user = "xxxxxxx",
        password = "xxxxxxx",
        host = "45.79.xx.xxx",
        port= "5432",
        database = "doomsday"
            )
        cursor = connection.cursor()

    except (Exception, psycopg2.Error) as error:
        print(error)

    query =  "INSERT INTO threats (threat, insert_date) VALUES (%s, %s);"
    data = (record, datetime.now())
    try:
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        print(error)


spark = SparkSession \
            .builder \
            .appName("StructuredThreats") \
            .master("local[*]") \
            .getOrCreate()

threatsDataFrame = spark \
                   .readStream \
                   .csv(path="file:///home/hadoop/doomsday/threats/",
                        schema= fileschema,
                        sep=",",
                        header=False)

query = threatsDataFrame.writeStream.foreach(insert_record).trigger(processingTime='5 seconds').start()
query.awaitTermination()
