use todo_db;

// 创建列表集合
db.createCollection("todo_lists");

// 创建项集合
db.createCollection("todo_items");

// 插入测试列表（关联用户ID=1）
db.todo_lists.insertOne({
    list_id: "list_test_001",
    owner_id: "1",
    title: "开发任务",
    description: "API开发相关任务",
    created_at: new Date(),
    updated_at: new Date()
});

// 插入测试项
db.todo_items.insertOne({
    item_id: "item_test_001",
    list_id: "list_test_001",
    title: "完成控制器代码",
    description: "实现TODO项的CRUD接口",
    due_date: new Date("2024-12-31"),
    status: "In Progress",
    priority: "High",
    tags: ["开发", "紧急"],
    created_at: new Date(),
    updated_at: new Date()
});

// 创建索引
db.todo_items.createIndex({ list_id: 1 });