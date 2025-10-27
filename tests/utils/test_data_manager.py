import json
import os
from typing import Dict, Any

class TestDataManager:
    DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data.json')

    @classmethod
    def save_data(cls, data: Dict[str, Any]) -> None:
        """保存测试数据到文件"""
        with open(cls.DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_data(cls) -> Dict[str, Any]:
        """从文件加载测试数据"""
        if not os.path.exists(cls.DATA_FILE):
            return {}
        with open(cls.DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def update_data(cls, key: str, value: Any) -> None:
        """更新特定键的数据"""
        data = cls.load_data()
        data[key] = value
        cls.save_data(data)

    @classmethod
    def get_value(cls, key: str, default: Any = None) -> Any:
        """获取特定键的数据"""
        data = cls.load_data()
        return data.get(key, default)

    @classmethod
    def clear_data(cls) -> None:
        """清除所有测试数据"""
        if os.path.exists(cls.DATA_FILE):
            os.remove(cls.DATA_FILE)