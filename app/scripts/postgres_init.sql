-- 创建用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建权限表
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    list_id VARCHAR(50) NOT NULL,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    perm_type VARCHAR(20) NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(list_id, user_id)
);

-- 插入测试用户（密码：test123）
INSERT INTO users (email, password_hash, full_name, role)
VALUES (
    'test@example.com',
    '$2b$12$EixZaYb051aW720b7h2f4.2t0y0G9w5K6R5D8F7S1A2D3F4G5H6J7',
    'Test User',
    'USER'
);