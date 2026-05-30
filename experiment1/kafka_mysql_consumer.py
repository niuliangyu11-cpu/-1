import json
from kafka import KafkaConsumer

# Kafka消费者配置
consumer = KafkaConsumer(
    'student-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='student-group'
)

def consume_student_data():
    """从Kafka消费学生数据并输出"""
    print("开始消费学生数据...")
    for message in consumer:
        print(f"接收到数据: {message.value}")

if __name__ == "__main__":
    consume_student_data()
