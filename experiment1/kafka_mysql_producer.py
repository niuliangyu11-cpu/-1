import json
import mysql.connector
from kafka import KafkaProducer
from kafka.errors import KafkaError

# MySQL连接配置
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'your_database'
}

# Kafka生产者配置
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_and_send_student_data():
    """读取MySQL学生表数据并发送到Kafka"""
    try:
        # 连接MySQL
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # 查询学生表数据
        cursor.execute("SELECT sno, sname, ssex, sage FROM student")
        students = cursor.fetchall()
        
        # 将数据发送给Kafka
        for student in students:
            print(f"发送数据: {student}")
            producer.send('student-topic', value=student)
        
        producer.flush()
        print("所有数据发送完成")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    read_and_send_student_data()
