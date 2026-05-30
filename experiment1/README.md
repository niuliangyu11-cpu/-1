# 实验1：Kafka与MySQL的组合使用

## 实验目标
- 从MySQL数据库读取学生表数据
- 将数据转为JSON格式发送给Kafka
- 从Kafka消费JSON格式数据并输出

## 前置条件

### 1. 创建MySQL数据库和student表

```sql
-- 创建数据库
CREATE DATABASE your_database;
USE your_database;

-- 创建student表
CREATE TABLE student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50),
    ssex CHAR(1),
    sage INT
);

-- 插入测试数据
INSERT INTO student VALUES 
(95001, 'John', 'M', 23),
(95002, 'Tom', 'M', 23);
```

### 2. 创建Kafka主题

```bash
cd /usr/local/kafka

./bin/kafka-topics.sh --create --topic student-topic \
  --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
```

### 3. 安装Python依赖

```bash
pip install kafka-python mysql-connector-python
```

## 配置

修改 `kafka_mysql_producer.py` 中的MySQL连接配置：

```python
mysql_config = {
    'host': 'localhost',      # MySQL服务器地址
    'user': 'root',           # MySQL用户名
    'password': 'your_password',  # MySQL密码
    'database': 'your_database'   # 数据库名称
}
```

## 运行程序

### 方式1：分别启动生产者和消费者

**终端1：启动消费者**（先启动，等待数据）
```bash
python kafka_mysql_consumer.py
```

**终端2：启动生产者**
```bash
python kafka_mysql_producer.py
```

### 方式2：同步启动

```bash
# 终端1
python kafka_mysql_consumer.py

# 终端2
python kafka_mysql_producer.py
```

## 预期输出

### 生产者输出
```
发送数据: {'sno': 95001, 'sname': 'John', 'ssex': 'M', 'sage': 23}
发送数据: {'sno': 95002, 'sname': 'Tom', 'ssex': 'M', 'sage': 23}
所有数据发送完成
```

### 消费者输出
```
开始消费学生数据...
接收到数据: {'sno': 95001, 'sname': 'John', 'ssex': 'M', 'sage': 23}
接收到数据: {'sno': 95002, 'sname': 'Tom', 'ssex': 'M', 'sage': 23}
```

## 常用命令

### 查看主题
```bash
./bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 查看主题详情
```bash
./bin/kafka-topics.sh --describe --topic student-topic \
  --bootstrap-server localhost:9092
```

### 使用CLI��费消息
```bash
./bin/kafka-console-consumer.sh --topic student-topic \
  --bootstrap-server localhost:9092 --from-beginning
```

### 删除主题
```bash
./bin/kafka-topics.sh --delete --topic student-topic \
  --bootstrap-server localhost:9092
```

## 故障排除

### 1. 连接MySQL失败
- 检查MySQL服务是否启动
- 验证用户名和密码
- 确认数据库名称正确

### 2. 连接Kafka失败
- 检查Kafka服务是否启动
- 验证Bootstrap Server地址和端口
- 确认主题是否存在

### 3. 消费者没有收到数据
- 确保生产者成功发送数据
- 检查消费者组ID是否一致
- 尝试使用 `--from-beginning` 参数重新消费

## 文件说明

| 文件 | 说明 |
|------|------|
| `kafka_mysql_producer.py` | 生产者程序，从MySQL读取数据并发送到Kafka |
| `kafka_mysql_consumer.py` | 消费者程序，从Kafka消费数据并输出 |
| `README.md` | 实验说明文档 |

## 参考资源

- [Kafka官方文档](https://kafka.apache.org/documentation/)
- [kafka-python库文档](https://kafka-python.readthedocs.io/)
- [MySQL Connector/Python文档](https://dev.mysql.com/doc/connector-python/en/)
