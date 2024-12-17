from pyspark.sql import SparkSession
from pyspark.sql.functions import struct, lit, col, lower, regexp_replace, expr, regexp_extract, udf, transform, trim, explode, split, count, collect_list, concat_ws, size, filter, pandas_udf, broadcast
from nltk.stem import PorterStemmer
from pyspark.sql.functions import col, flatten, collect_list
from pyspark.sql import functions as F


spark = SparkSession.builder \
    .appName("Spark XML Example") \
    .config("spark.jars", 'C:\SPARK\spark-xml_2.12-0.16.0.jar') \
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:4.4.3") \
    .config("spark.jars.repositories", "https://repo1.maven.org/maven2/") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .master("local[*]") \
    .getOrCreate()

# Đọc dữ liệu
old_df = spark.read.parquet("parquetFile/final.parquet")
inverted_index_with_count = spark.read.parquet("parquetFile/final2.parquet")

# Đổi tên các cột locations để tránh bị nhầm lẫn sau khi join
old_df = old_df.withColumnRenamed("locations", "locations_old")
inverted_index_with_count = inverted_index_with_count.withColumnRenamed("locations", "locations_new")

# Thực hiện join giữa hai bảng theo cột "word"
combined_df = old_df.join(broadcast(inverted_index_with_count), "word", "outer")
combined_df.show()

# Group theo "word" và gom tất cả các locations từ cả hai cột vào một danh sách duy nhất
combined_df_grouped = combined_df.groupBy("word").agg(
    # Kết hợp cả hai cột locations_old và locations_new thành một danh sách duy nhất
    F.flatten(F.array_union(F.collect_list("locations_old"), F.collect_list("locations_new"))).alias("locations")
)

# Hiển thị kết quả
combined_df_grouped.show(truncate=False)

combined_df_grouped.write.mode("overwrite").parquet("hdfs://namenode:9000/user/root/index/final.parquet")

spark.stop()