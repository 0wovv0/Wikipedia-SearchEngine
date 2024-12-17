from sparknlp.pretrained import PretrainedPipeline
from sparknlp.annotator import Tokenizer, LemmatizerModel
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
# Thử tải một pipeline đơn giản để kiểm tra kết nối và mô hình
try:
    lemmatizer = LemmatizerModel.pretrained("lemma")
    print("Mô hình đã được tải thành công!")
except Exception as e:
    print("Lỗi khi tải mô hình:", e)
