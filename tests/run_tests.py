#!/usr/bin/env python3
"""
测试运行脚本
用于运行集成测试并生成测试报告
"""
import subprocess
import sys
import os
from pathlib import Path


def run_tests():
    """运行所有测试"""
    print("🚀 开始运行TODO API集成测试...")
    print("=" * 60)
    
    # 确保在正确的目录
    test_dir = Path(__file__).parent
    os.chdir(test_dir)
    
    # 运行测试命令
    cmd = [
        sys.executable, "-m", "pytest",
        "integration/",
        "-v",  # 详细输出
        "--tb=short",  # 简短的错误跟踪
        "--color=yes",  # 彩色输出
        "--durations=10",  # 显示最慢的10个测试
        "-x",  # 遇到第一个失败就停止
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ 所有测试通过！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 测试失败，退出码: {e.returncode}")
        return False


def run_specific_test(test_name: str):
    """运行特定的测试"""
    print(f"🎯 运行特定测试: {test_name}")
    print("=" * 60)
    
    test_dir = Path(__file__).parent
    os.chdir(test_dir)
    
    cmd = [
        sys.executable, "-m", "pytest",
        f"integration/{test_name}",
        "-v",
        "--tb=short",
        "--color=yes",
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ 测试 {test_name} 通过！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 测试 {test_name} 失败，退出码: {e.returncode}")
        return False


def show_test_list():
    """显示所有可用的测试"""
    print("📋 可用的测试用例:")
    print("=" * 60)
    
    test_files = [
        ("test_auth_api.py", "认证API测试", [
            "test_register_success", "test_register_duplicate_email", "test_register_missing_field",
            "test_register_weak_password", "test_login_success", "test_login_invalid_password",
            "test_login_nonexistent_user", "test_login_missing_field", "test_token_validation",
            "test_invalid_token", "test_no_token", "test_data_manager_functionality"
        ]),
        ("test_todo_list_api.py", "待办列表API测试", [
            "test_todo_list_create_success", "test_todo_list_create_unauthorized", "test_todo_list_create_missing_title",
            "test_todo_list_get_all", "test_todo_list_get_single_success", "test_todo_list_get_other_user_list",
            "test_todo_list_get_nonexistent", "test_todo_list_update_success", "test_todo_list_update_other_user",
            "test_todo_list_delete_success", "test_todo_list_delete_other_user", "test_todo_list_delete_nonexistent",
            "test_todo_list_create_empty_title", "test_todo_list_create_title_too_long", "test_todo_list_create_description_too_long",
            "test_todo_list_update_partial", "test_todo_list_get_empty_list", "test_todo_list_create_without_description",
            "test_todo_list_update_nonexistent", "test_cross_user_data_isolation"
        ]),
        ("test_todo_item_api.py", "待办事项API测试", [
            "test_todo_item_create_success", "test_todo_item_create_unauthorized", "test_todo_item_create_missing_title",
            "test_todo_item_create_invalid_list", "test_todo_item_get_all", "test_todo_item_get_single_success",
            "test_todo_item_get_other_user_list", "test_todo_item_get_nonexistent", "test_todo_item_update_success",
            "test_todo_item_update_other_user", "test_todo_item_delete_success", "test_todo_item_delete_other_user",
            "test_todo_item_delete_nonexistent", "test_todo_item_create_empty_title", "test_todo_item_create_without_description",
            "test_todo_item_update_partial", "test_todo_item_get_empty_list", "test_todo_item_update_nonexistent",
            "test_todo_item_filter_by_status", "test_todo_item_sort_by_due_date"
        ])
    ]
    
    total_tests = 0
    for file_name, description, tests in test_files:
        print(f"\n📁 {file_name} - {description}")
        for i, test_name in enumerate(tests, 1):
            print(f"  {i:2d}. {test_name}")
        total_tests += len(tests)
    
    print(f"\n总计: {total_tests} 个测试用例")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            show_test_list()
        elif command == "run":
            if len(sys.argv) > 2:
                test_name = sys.argv[2]
                success = run_specific_test(test_name)
            else:
                success = run_tests()
            sys.exit(0 if success else 1)
        else:
            print("❌ 未知命令")
            print("可用命令:")
            print("  python run_tests.py list     - 显示所有测试")
            print("  python run_tests.py run      - 运行所有测试")
            print("  python run_tests.py run <test_file> - 运行特定测试文件")
            sys.exit(1)
    else:
        print("🔧 TODO API 测试运行器")
        print("=" * 60)
        print("用法:")
        print("  python run_tests.py list     - 显示所有测试")
        print("  python run_tests.py run      - 运行所有测试")
        print("  python run_tests.py run <test_file> - 运行特定测试文件")
        print("\n示例:")
        print("  python run_tests.py run test_auth_api.py")
        print("  python run_tests.py run test_todo_list_api.py")
        print("  python run_tests.py run test_todo_item_api.py")


if __name__ == "__main__":
    main()
