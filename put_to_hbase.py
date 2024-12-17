from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import happybase
from pyspark.sql.functions import col, regexp_replace, lower, trim


# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Wiki XML") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "4g") \
    .config("spark.hadoop.hbase.zookeeper.quorum", "zookeeper") \
    .config("spark.hadoop.hbase.zookeeper.property.clientPort", "2181") \
    .config("spark.hadoop.hbase.master", "hbase-master") \
    .getOrCreate()

PATH_TO_FILE = '/user/root/input/wiki-dum.xml'
df = spark.read.format("xml").option("rowTag", "page").option("inferSchema", "true").load('hdfs://namenode:9000' + PATH_TO_FILE)

df = df.withColumn(
    "title",
    lower(trim(regexp_replace(regexp_replace(col("title"), r'[^\w\s]', ' '), r'\s+', ' ')))
)

df_flat = df.select(
    col("id"),
    col("ns"),
    col("redirect._VALUE").alias("redirect_value"),
    col("redirect._title").alias("redirect_title"),
    col("revision.comment").alias("revision_comment"),
    col("revision.contributor.id").alias("contributor_id"),
    col("revision.contributor.ip").alias("contributor_ip"),
    col("revision.contributor.username").alias("contributor_username"),
    col("revision.format").alias("revision_format"),
    col("revision.id").alias("revision_id"),
    col("revision.minor").alias("revision_minor"),
    col("revision.model").alias("revision_model"),
    col("revision.origin").alias("revision_origin"),
    col("revision.parentid").alias("revision_parentid"),
    col("revision.sha1").alias("revision_sha1"),
    col("revision.text._VALUE").alias("content"),
    col("revision.text._bytes").alias("text_bytes"),
    col("revision.text._sha1").alias("text_sha1"),
    col("revision.text._xml:space").alias("text_xml_space"),
    col("revision.timestamp").alias("timestamp"),
    col("title")
)



df.show()

# df_flat = df_flat.withColumn("redirect_title", coalesce(df_flat["redirect_title"], df_flat["title"]))
# print(f'Number of rows: {df_flat.count()}')
# df_flat.show(5, truncate=False)
# Function to write data to HBase
def write_to_hbase(partition):
    connection = happybase.Connection('hbase-master')
    connection.open()
    table = connection.table('wikipedia')
    
    for row in partition:
        row_key = str(row["title"]).encode('utf-8') if row["title"] else b'unknown'

        table.put(row_key, {
            b'cf:title': str(row["title"]).encode('utf-8') if row["title"] else b'',
            b'cf:id': str(row["id"]).encode('utf-8') if row["id"] else b'',
            b'cf:ns': str(row["ns"]).encode('utf-8') if row["ns"] else b'',
            b'cf:redirect_value': str(row["redirect_value"]).encode('utf-8') if row["redirect_value"] else b'',
            b'cf:redirect_title': str(row["redirect_title"]).encode('utf-8') if row["redirect_title"] else b'',
            b'cf:revision_comment': str(row["revision_comment"]).encode('utf-8') if row["revision_comment"] else b'',
            b'cf:contributor_id': str(row["contributor_id"]).encode('utf-8') if row["contributor_id"] else b'',
            b'cf:contributor_ip': str(row["contributor_ip"]).encode('utf-8') if row["contributor_ip"] else b'',
            b'cf:contributor_username': str(row["contributor_username"]).encode('utf-8') if row["contributor_username"] else b'',
            b'cf:revision_format': str(row["revision_format"]).encode('utf-8') if row["revision_format"] else b'',
            b'cf:revision_id': str(row["revision_id"]).encode('utf-8') if row["revision_id"] else b'',
            b'cf:revision_minor': str(row["revision_minor"]).encode('utf-8') if row["revision_minor"] else b'',
            b'cf:revision_model': str(row["revision_model"]).encode('utf-8') if row["revision_model"] else b'',
            b'cf:revision_origin': str(row["revision_origin"]).encode('utf-8') if row["revision_origin"] else b'',
            b'cf:revision_parentid': str(row["revision_parentid"]).encode('utf-8') if row["revision_parentid"] else b'',
            b'cf:revision_sha1': str(row["revision_sha1"]).encode('utf-8') if row["revision_sha1"] else b'',
            b'cf:revision_timestamp': str(row["timestamp"]).encode('utf-8') if row["timestamp"] else b'',
            b'cf:revision_text_VALUE': str(row["content"]).encode('utf-8') if row["content"] else b'',
            b'cf:revision_text_bytes': str(row["text_bytes"]).encode('utf-8') if row["text_bytes"] else b'',
            b'cf:revision_text_sha1': str(row["text_sha1"]).encode('utf-8') if row["text_sha1"] else b'',
            b'cf:revision_text_xmlspace': str(row["text_xml_space"]).encode('utf-8') if row["text_xml_space"] else b'',
        })

    connection.close()
    print("Data written to HBase\n")
    

# Map each row to records for writing to HBase
df_flat.rdd.foreachPartition(write_to_hbase)