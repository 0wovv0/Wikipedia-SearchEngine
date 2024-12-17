import re
import happybase
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import ast
import pandas as pd


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
    table3 = connection.table('index')
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
        key_words = user_query.split()

        # Giả sử key_words và table đã được định nghĩa
        rows = []
        for key in key_words:
            row = table3.row(key.encode('utf-8'))  # Lấy dòng từ HBase dựa trên row_key
            for key_, value_ in row.items():
                data_list = ast.literal_eval(value_.decode('utf-8'))  # Chuyển đổi từ string thành list
                rows.append({"word": key, "locations": data_list})  # Lưu key và data_list vào rows

        # Tạo DataFrame từ list rows
        df = pd.DataFrame(rows)
        print(df, "\n")

        # Bước 1: Explode cột 'locations'
        if 'locations' in df.columns:
            exploded_df = df.explode('locations')
        else:
            print("Cột 'locations' không tồn tại trong DataFrame!")
            exploded_df = pd.DataFrame()  # Tạo DataFrame rỗng để tránh lỗi


        # Bước 2: Tách list con thành các cột riêng
        exploded_df[['doc_id', 'location', 'frequency']] = pd.DataFrame(exploded_df['locations'].tolist(), index=exploded_df.index)

        # Bước 3: Tính điểm dựa trên điều kiện vị trí
        def calculate_score(row):
            if row['location'] == 'revision_comment':
                return row['frequency'] * 5
            elif row['location'] == 'title':
                return row['frequency'] * 150
            else:
                return row['frequency'] * 1

        exploded_df['score'] = exploded_df.apply(calculate_score, axis=1)

        # Bước 4: Tính tổng điểm cho mỗi 'doc_id'
        aggregated_df = exploded_df.groupby('doc_id', as_index=False)['score'].sum()
        aggregated_df = aggregated_df.rename(columns={'score': 'total_score'})

        # Bước 5: Sắp xếp và lấy top 3 bài viết có điểm cao nhất
        top_3_ids = aggregated_df.sort_values(by='total_score', ascending=False).head(3)

        # Hiển thị kết quả
        print("Top 3 bài viết có tổng điểm cao nhất:")
        print(top_3_ids)

        # Lấy dòng có tổng điểm cao nhất
        highest_score_row = aggregated_df.loc[aggregated_df['total_score'].idxmax()]

        # Trích xuất doc_id có điểm cao nhất
        row_key = highest_score_row['doc_id']
        
        # Retrieve the row with the row key 'United States'
        # row_key = 'anarchism'
        # Lưu vào HBase
        # Lưu top 3 hoặc ít hơn nếu không có đủ dữ liệu
        top_count = len(top_3_ids)

        # table2.put(user_query.encode('utf-8'), {
        #     b'cf:top1': str(top_3_ids.iloc[0]["doc_id"]).encode('utf-8') if top_count > 0 else b'',
        #     b'cf:top2': str(top_3_ids.iloc[1]["doc_id"]).encode('utf-8') if top_count > 1 else b'',
        #     b'cf:top3': str(top_3_ids.iloc[2]["doc_id"]).encode('utf-8') if top_count > 2 else b'',
        #     b'cf:top4': str(top_3_ids.iloc[3]["doc_id"]).encode('utf-8') if top_count > 3 else b'',
        #     b'cf:top5': str(top_3_ids.iloc[4]["doc_id"]).encode('utf-8') if top_count > 4 else b''
        # })

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