from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col, explode
import re
from pyspark.sql.functions import when, sum
import happybase
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template

spark = SparkSession.builder \
    .appName("Wiki XML") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "4g") \
    .config("spark.hadoop.hbase.zookeeper.quorum", "zookeeper") \
    .config("spark.hadoop.hbase.zookeeper.property.clientPort", "2181") \
    .config("spark.hadoop.hbase.master", "hbase-master") \
    .getOrCreate()
    
df = spark.read.parquet("hdfs://namenode:9000/user/root/index/final.parquet")
df.show()

app = Flask(__name__)
CORS(app)  # Cho phép CORS trên toàn bộ ứng dụng

# Connect to HBase
connection = happybase.Connection('hbase-master')
connection.open()
table2 = connection.table('top_scores')
table = connection.table('wikipedia')

# Tạo endpoint để phục vụ trang web chính
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def process_query():
    # # Nhận truy vấn dạng user_query từ client
    user_query = request.json.get("query", "")
    
    import re

    # Bước 1: Chuyển tất cả ký tự về chữ thường
    user_query = user_query.lower()

    # Bước 2: Thay thế ký tự đặc biệt bằng khoảng trắng
    user_query = re.sub(r"[^a-zA-Z0-9]", " ", user_query)

    # Bước 3: Tách chuỗi thành danh sách các từ
    key_words = user_query.split()

    result_df = df.filter(col("word").isin(key_words))

    # Tách cột locations (explode để xử lý từng phần tử)
    exploded_df = result_df.withColumn("location_item", explode(col("locations")))

    # Trích xuất các trường từ StructType trong cột locations
    processed_df = exploded_df.select(
        col("word"),
        col("location_item.doc_id").alias("doc_id"),
        col("location_item.location").alias("position"),
        col("location_item.frequency").alias("count")
    )

    # Tính điểm dựa trên vị trí
    scored_df = processed_df.withColumn(
        "score",
        when(col("position") == "revision_comment", col("count") * 5)
        .when(col("position") == "title", col("count") * 150)
        .otherwise(col("count") * 1)
    )

    # Tính tổng điểm cho mỗi bài viết (doc_id)
    aggregated_df = scored_df.groupBy("doc_id").agg(sum("score").alias("total_score"))

    # Sắp xếp theo tổng điểm và lấy top 3 bài viết có điểm cao nhất
    top_3_ids = aggregated_df.orderBy(col("total_score").desc()).limit(5)

    # Hiển thị kết quả
    top_3_ids.show(truncate=False)
            
    try:
        print(user_query)
        # Thực hiện lọc trên DataFrame dựa vào truy vấn
        return jsonify({"status": "success", "data": user_query})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Close the connection
# connection.close()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)