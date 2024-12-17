import requests

def click_and_download(url):
    try:
        # Gửi yêu cầu GET tới URL
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        # Lấy tên file từ tiêu đề hoặc URL
        filename = "file.bz2" # Lấy phần cuối của URL làm tên file
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        print(f"File đã được tải xuống và lưu với tên: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Đã xảy ra lỗi: {e}")

# Sử dụng hàm
url = "https://dumps.wikimedia.org/enwiki/20240901/enwiki-20240901-pages-articles-multistream-index4.txt-p311330p558391.bz2"  # Thay bằng URL của bạn
click_and_download(url)

import bz2

def extract_bz2(input_path, output_path):
    try:
        with bz2.BZ2File(input_path, 'rb') as file_in:
            with open(output_path, 'wb') as file_out:
                file_out.write(file_in.read())
        print(f"File đã được giải nén: {output_path}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Sử dụng hàm
input_file = "file.bz2"
output_file = "wiki-dum2.xml"
extract_bz2(input_file, output_file)

import subprocess

def upload_to_hdfs(local_path, hdfs_path):
    try:
        # Chạy lệnh hdfs dfs -put
        subprocess.run(["hdfs", "dfs", "-put", local_path, hdfs_path], check=True)
        print(f"File {local_path} đã được upload lên HDFS tại {hdfs_path}")
    except subprocess.CalledProcessError as e:
        print(f"Đã xảy ra lỗi khi upload file lên HDFS: {e}")

# Sử dụng hàm
local_file = "wiki-dum2.xml"  # Đường dẫn file trên máy
hdfs_directory = "/user/hadoop/input/"  # Đường dẫn thư mục HDFS
upload_to_hdfs(local_file, hdfs_directory)

