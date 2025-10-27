"""
简化的测试数据管理器
只保存测试过程中重要的ID和token
"""
from typing import Dict, Optional


class TestDataManager:
    """简化的测试数据管理器"""

    def __init__(self):
        self.data: Dict[str, str] = {}

    def save_token(self, user_key: str, access_token: str) -> None:
        """保存访问令牌"""
        self.data[f"{user_key}_token"] = access_token

    def save_user_id(self, user_key: str, user_id: str) -> None:
        """保存用户ID"""
        self.data[f"{user_key}_user_id"] = user_id

    def save_list_id(self, list_key: str, list_id: str) -> None:
        """保存列表ID"""
        self.data[f"{list_key}_list_id"] = list_id

    def save_item_id(self, item_key: str, item_id: str) -> None:
        """保存待办事项ID"""
        self.data[f"{item_key}_item_id"] = item_id

    def get_token(self, user_key: str) -> Optional[str]:
        """获取访问令牌"""
        return self.data.get(f"{user_key}_token")

    def get_user_id(self, user_key: str) -> Optional[str]:
        """获取用户ID"""
        return self.data.get(f"{user_key}_user_id")

    def get_list_id(self, list_key: str) -> Optional[str]:
        """获取列表ID"""
        return self.data.get(f"{list_key}_list_id")

    def get_item_id(self, item_key: str) -> Optional[str]:
        """获取待办事项ID"""
        return self.data.get(f"{item_key}_item_id")

    def get_auth_headers(self, user_key: str) -> Optional[Dict[str, str]]:
        """获取认证头"""
        token = self.get_token(user_key)
        if not token:
            return None
        return {"Content-Type": "application/json",
                "Authorization": "Bearer " + str(token)}

    def clear_all(self) -> None:
        """清理所有数据"""
        self.data.clear()

    def get_summary(self) -> Dict[str, int]:
        """获取数据摘要"""
        tokens = len([k for k in self.data.keys() if k.endswith("_token")])
        user_ids = len([k for k in self.data.keys() if k.endswith("_user_id")])
        list_ids = len([k for k in self.data.keys() if k.endswith("_list_id")])
        item_ids = len([k for k in self.data.keys() if k.endswith("_item_id")])

        return {
            "tokens": tokens,
            "user_ids": user_ids,
            "list_ids": list_ids,
            "item_ids": item_ids,
            "total": len(self.data)
        }


# 全局测试数据管理器实例
test_data_manager = TestDataManager()
