use todo_db
db.createCollection("todo_lists")
db.createCollection("todo_items")
db.todo_lists.insertOne({
    list_id: "list_test_001",
    owner_id: "1",
    title: "deve",
    description: "sddfsdf",
    created_at: new Date(),
    updated_at: new Date()
})
db.todo_items.insertOne({
    item_id: "item_test_001",
    list_id: "list_test_001",
    title: "sdf12312312",
    description: "3434234234",
    due_date: new Date("2024-12-31"),
    status: "In Progress",
    priority: "High",
    tags: ["111", "2222"],
    created_at: new Date(),
    updated_at: new Date()
})
db.todo_items.createIndex({ list_id: 1 })