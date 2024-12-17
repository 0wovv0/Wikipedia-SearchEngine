from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Định nghĩa các Spark job
def run_spark_job_1():
    """Chạy Spark job 1"""
    subprocess.run(['spark-submit', 'crawl.py'], check=True)

def run_spark_job_2():
    """Chạy Spark job 2"""
    subprocess.run(['spark-submit', 'put_to_hbase.py'], check=True)

def run_spark_job_3():
    """Chạy Spark job 3"""
    subprocess.run(['spark-submit', 'extract.py'], check=True)

# Khai báo tham số mặc định cho DAG
default_args = {
    'owner': 'airflow',  # Người sở hữu DAG
    'retries': 1,  # Số lần thử lại nếu job thất bại
    'retry_delay': timedelta(minutes=5),  # Độ trễ giữa các lần thử lại
    'start_date': datetime(2024, 12, 17),  # Thời gian bắt đầu DAG
    'catchup': False,  # Không chạy các task đã bỏ lỡ trước thời điểm start_date
    'depends_on_past': True,  # Phụ thuộc vào task trước đó
    'email_on_failure': False,  # Không gửi email khi task thất bại
    'email_on_retry': False,  # Không gửi email khi task thử lại
}

# Tạo DAG
dag = DAG(
    'spark_jobs_dag',  # Tên DAG
    default_args=default_args,  # Tham số mặc định
    description='DAG để chạy các Spark job',
    schedule_interval='@daily',  # Lịch chạy DAG, ví dụ: chạy mỗi ngày
    catchup=False,  # Không chạy các task đã bỏ lỡ
)

# Khai báo các task trong DAG
task_1 = PythonOperator(
    task_id='crawl',  # Tên của task
    python_callable=run_spark_job_1,  # Hàm Python gọi Spark job 1
    dag=dag,  # DAG mà task thuộc về
)

task_2 = PythonOperator(
    task_id='put_to_hbase',  # Tên của task
    python_callable=run_spark_job_2,  # Hàm Python gọi Spark job 2
    dag=dag,  # DAG mà task thuộc về
)

task_3 = PythonOperator(
    task_id='extract',  # Tên của task
    python_callable=run_spark_job_3,  # Hàm Python gọi Spark job 3
    dag=dag,  # DAG mà task thuộc về
)

# Thiết lập thứ tự thực hiện các task trong DAG
task_1 >> task_2 >> task_3  # Task 1 chạy trước, sau đó task 2, và cuối cùng task 3
