from pyspark.sql import SparkSession
import happybase
import json

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Wiki XML") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "4g") \
    .config("spark.hadoop.hbase.zookeeper.quorum", "zookeeper") \
    .config("spark.hadoop.hbase.zookeeper.property.clientPort", "2181") \
    .config("spark.hadoop.hbase.master", "hbase-master") \
    .getOrCreate()

df_flat = spark.read.parquet('hdfs://namenode:9000/user/root/index/final.parquet')

# Function to write DataFrame to HBase using batch processing
def write_to_hbase(partition):
    connection = happybase.Connection('hbase-master')
    connection.open()
    table = connection.table('index')  # Name of your HBase table

    # Use batch processing to group writes
    with table.batch() as batch:
        for row in partition:
            word = str(row["word"]).encode('utf-8')  # Row key (word)
            locations = row["locations"]  # Locations as a list of dictionaries

            # Convert locations to JSON string
            locations_json = json.dumps(locations)

            # Prepare the data to be written into HBase
            data = {
                b'locations:locations': locations_json.encode('utf-8')  # Store locations as JSON in the 'locations' column family
            }

            # Add data to the batch
            batch.put(word, data)

    connection.close()
    print("Data written to HBase")
df_flat = df_flat.repartition(100)

# Assuming df is your DataFrame with 'word' and 'locations' columns
df_flat.rdd.foreachPartition(write_to_hbase)
