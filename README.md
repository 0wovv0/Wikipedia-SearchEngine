# Wikipedia Search Engine

## Giới thiệu
Dự án Wikipedia Search Engine là một công cụ tìm kiếm mạnh mẽ được xây dựng trên nền tảng tập dữ liệu 75 GB từ Wikipedia. Công cụ này sử dụng thuật toán TF-IDF để xếp hạng các trang dựa trên độ liên quan đến từ khóa tìm kiếm.

## Tính năng
- Tìm kiếm nhanh với độ trễ dưới 1 giây cho truy vấn đơn giản.
- Xếp hạng kết quả dựa trên độ liên quan với TF-IDF.
- Hỗ trợ tìm kiếm cho các từ khóa phức tạp.

## Công nghệ sử dụng
- Python
- PySpark
- Hadoop
- TF-IDF
# Quick Setup

B1: Chuẩn bị file wiki_dump

B2: Chạy các container

```
  docker-compose up -d
```

Đối với lần đầu sử dụng hoặc muốn build lại các container

```
  docker-compose up --build -d
```

B3: Copy file wiki_dump vào hdfs để spark có thể sử dụng

  - Tạo thư mục để lưu file

```
  docker exec -it namenode hdfs dfs -mkdir -p /user/root/input
```
  - Copy file dump vào hdfs:

```
  docker cp /path/to/your_file namenode:/tmp
  docker exec -it namenode hdfs dfs -put /tmp/file_name /user/root/input
```  

B4: Sử dụng Spark tạo danh sách indexes của các từ và lưu vào Hadoop
  - Thay đổi đường dẫn trong file extract_info tại dòng 9

  - Copy file xử lý vào Spark:

```
  docker cp extract.py spark-master:/tmp
```
  - Chạy file xử lý với spark-submit

```
    docker exec -it spark-master /spark/bin/spark-submit /tmp/extract.py
```
Sau khi chạy xong lệnh trên, danh sách chỉ mục sẽ được lưu trữ trên hadoop.

Truy cập địa chỉ: http://localhost:9870, lựa chọn "Utilities" (trên thanh công cụ) -> "Browse the file system" -> chọn thư mục "user" -> "root" -> "indexes"

# Quick Search

B1: thay từ cần tìm kiếm trong file search.py dòng 7

B2: Copy file vào Spark-master container

```
docker cp search.py spark-master:/tmp
```
B3: Chạy file search và nhận kết quả

```
docker exec -it spark-master /spark/bin/spark-submit /tmp/search.py
```

# Xóa các container
```
docker-compose down
```
# Note
- Mở cmd tại đúng thư mục dự án để có thể chạy các docker containers
- Kiểm tra các Session của Spark tại: http://localhost:8080
- Mỗi lần tắt các Docker Container thì các file xử lý và tìm kiếm dữ liệu sẽ mất và phải copy lại vào Spark-master nhưng dữ liệu ở hadoop vẫn được dữ nguyên
