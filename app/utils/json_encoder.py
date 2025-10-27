from datetime import datetime, date
from bson import ObjectId


def process_data(data):
    """
    递归处理数据中的复杂类型，转换为JSON可序列化格式
    支持：字典、列表、datetime、date、ObjectId等
    """
    # 1. 如果是字典，递归处理每个值
    if isinstance(data, dict):
        return {k: process_data(v) for k, v in data.items()}

    # 2. 如果是列表/元组，递归处理每个元素
    elif isinstance(data, (list, tuple)):
        return [process_data(item) for item in data]

    # 3. 处理日期时间类型（包括MongoDB的bson.datetime）
    elif isinstance(data, (datetime, date)):
        return data.isoformat()

    # 4. 处理MongoDB的ObjectId
    elif isinstance(data, ObjectId):
        return str(data)

    # 5. 其他基础类型（字符串、数字等）直接返回
    else:
        return data