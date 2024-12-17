from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, expr, regexp_extract, udf, transform, trim, explode, split, count, collect_list, concat_ws, size, filter, pandas_udf
from pyspark.sql.types import StringType, StructType, StructField, ArrayType
from pyspark.sql.functions import coalesce
from pyspark.sql.functions import explode, split, col, lit
from pyspark.sql.functions import struct, collect_list
from pyspark import StorageLevel



spark = SparkSession.builder \
    .appName("Spark XML Example") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:4.4.3") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# from py4j.java_gateway import java_import
# java_import(spark._sc._jvm, "org.apache.spark.sql.api.python.*")

PATH_TO_FILE = 'hdfs://namenode:9000/user/root/input/wiki-dum.xml'

# Đọc XML với rowTag là "page"
df = spark.read.format("xml") \
    .option("rowTag", "page") \
    .option("inferSchema", "true") \
    .load(PATH_TO_FILE)

# Hiển thị schema để thấy các thẻ con
df.printSchema()

# df = df.repartition(6)

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
df_flat.repartition(3)
# Hiển thị kết quả
# Kiểm tra kiểu dữ liệu của 'revision.comment'
if not isinstance(df_flat.schema["revision_comment"].dataType, StringType):
    # Nếu không là chuỗi
    df_flat = df_flat.withColumn("revision_comment", col("revision_comment._VALUE"))

# df_flat = df_flat.withColumn("redirect_title", coalesce(df_flat["redirect_title"], df_flat["title"]))

# Áp dụng thao tác làm sạch và chuyển tất cả về chữ thường
df_flat = df_flat.withColumn(
    "content", 
    lower(trim(regexp_replace(regexp_replace(regexp_replace(col("content"), r'[^\w\s]', ' '), r'\s+', ' '), r'\d+', '')))
).withColumn(
    "revision_comment", 
    lower(trim(regexp_replace(regexp_replace(col("revision_comment"), r'[^\w\s]', ' '), r'\s+', ' ')))  # Xử lý comment
).withColumn(
    "title", 
    lower(trim(regexp_replace(regexp_replace(col("title"), r'[^\w\s]', ' '), r'\s+', ' ')))  # Xử lý comment
)

# Ghép dữ liệu từ nhiều cột
df_new = df_flat.select(
    col("title"),
    explode(
        split(col("title"), r"\s+")  # Tokenize Column1
    ).alias("word")
).withColumn("location", lit("title")) \
 .union(df_flat.select(
    col("title"),
    explode(
        split(col("revision_comment"), r"\s+")  # Tokenize Column2
    ).alias("word")
).withColumn("location", lit("revision_comment")))

df_new.persist(StorageLevel.DISK_ONLY)
df_new.show()

from sparknlp.pretrained import PretrainedPipeline
from sparknlp.annotator import Tokenizer, LemmatizerModel
from sparknlp.base import DocumentAssembler
from pyspark.ml import Pipeline

# Lưu mô hình vào thư mục cục bộ
# lemma = LemmatizerModel.pretrained("lemma_antbnc", lang="en")
# lemma.write().overwrite().save("/tmp/lemma_antbnc_model")

# Sử dụng mô hình đã lưu
lemmatizer = LemmatizerModel.pretrained("lemma_antbnc") \
    .setInputCols(["token"]) \
    .setOutputCol("lemma")


# Tạo DocumentAssembler
document_assembler = DocumentAssembler() \
    .setInputCol("word") \
    .setOutputCol("document")

# Tạo Tokenizer
tokenizer = Tokenizer() \
    .setInputCols(["document"]) \
    .setOutputCol("token")

# Xây dựng Pipeline
pipeline = Pipeline(stages=[
    document_assembler,
    tokenizer,
    lemmatizer
])

# Thực thi pipeline
model = pipeline.fit(df_new)
result = model.transform(df_new)

# Hiển thị kết quả
result.select("lemma.result").show(truncate=False)

from pyspark.sql.functions import col

# Thêm cột mới 'first_lemma' với phần tử đầu tiên của mảng 'lemma.result'
result = result.withColumn("first_lemma", col("lemma.result").getItem(0))

result = result.drop("token")
result = result.drop("document")
result = result.drop("lemma")
result = result.drop("word")
result = result.withColumnRenamed("first_lemma", "word")

# Đếm số lần xuất hiện của mỗi từ trong từng vị trí
df_count = result.groupBy("word", "title", "location").agg(
    count("*").alias("count")
)

# df_count.persist(StorageLevel.DISK_ONLY)

# Tổng hợp thành Inverted Index với số lần xuất hiện
inverted_index_with_count = df_count.groupBy("word").agg(
    collect_list(
        struct(
            col("title").alias("doc_id"),
            col("location"),
            col("count").alias("frequency")
        )
    ).alias("locations")
)

inverted_index_with_count.show(truncate=False)

print(f'Counttt :{inverted_index_with_count.count()}')

inverted_index_with_count.write.parquet("hdfs://namenode:9000/user/root/index/final.parquet")