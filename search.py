from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col, explode
import re
from pyspark.sql.functions import when, sum
import happybase
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import ast


spark = SparkSession.builder \
    .appName("Wiki XML") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "4g") \
    .config("spark.hadoop.hbase.zookeeper.quorum", "zookeeper") \
    .config("spark.hadoop.hbase.zookeeper.property.clientPort", "2181") \
    .config("spark.hadoop.hbase.master", "hbase-master") \
    .getOrCreate()

df = spark.read.parquet("hdfs://namenode:9000/user/root/index/final.parquet")

df.cache()

app = Flask(__name__)
CORS(app)  # Cho phép CORS trên toàn bộ ứng dụng

# Tạo endpoint để phục vụ trang web chính
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def process_query():
    
    # Connect to HBase
    connection = happybase.Connection('hbase-master')
    connection.open()
    table2 = connection.table('top_scores')
    table = connection.table('wikipedia')
    # Nhận truy vấn dạng user_query từ client
    user_query = request.json.get("search", "")
    
    # Bước 1: Chuyển tất cả ký tự về chữ thường
    user_query = user_query.lower()

    # Bước 2: Thay thế ký tự đặc biệt bằng khoảng trắng
    user_query = re.sub(r"[^a-zA-Z0-9]", " ", user_query)

    row2 = table2.row(user_query.encode('utf-8'))
    if row2:
        row_key = row2.get(b'cf:top1').decode('utf-8')  # Lấy giá trị cột 'top1'
        print("Ton tai ne!")

    else:
        print("khong ton tai ne!")
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

        # Get the table object
        first_row = top_3_ids.first()  # Lấy phần tử đầu tiên
        row_key = first_row["doc_id"] 
        # Retrieve the row with the row key 'United States'
        # row_key = 'anarchism'
        # Lưu vào HBase
        table2.put(user_query.encode('utf-8'), {
            b'cf:top1': str(top_3_ids.collect()[0]["doc_id"]).encode('utf-8'),  # top1
            b'cf:top2': str(top_3_ids.collect()[1]["doc_id"]).encode('utf-8'),  # top2
            b'cf:top3': str(top_3_ids.collect()[2]["doc_id"]).encode('utf-8'),   # top3
            b'cf:top4': str(top_3_ids.collect()[3]["doc_id"]).encode('utf-8'),  # top3
            b'cf:top5': str(top_3_ids.collect()[4]["doc_id"]).encode('utf-8')   # top3
        })

    row = table.row(row_key.encode('utf-8'))
    print(row)
    try:
        title = row.get(b'cf:title').decode('utf-8') if row.get(b'cf:title') else 'No Title'
        content = row.get(b'cf:revision_text_VALUE').decode('utf-8') if row.get(b'cf:revision_text_VALUE') else 'No Content'
        
        print(title, content)  # In ra để kiểm tra giá trị

        # Trả về giá trị dưới dạng JSON
        return jsonify({"title": title, "text": content})
    except Exception as e:
        # In lỗi nếu có
        print(f"Error: {e}")
        return jsonify({"title": "error", "text": "== Some error occurred! =="})
    finally:
        connection.close()
# connection.close()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)