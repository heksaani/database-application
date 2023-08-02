CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_leader BOOLEAN DEFAULT FALSE
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    leader_id INTEGER REFERENCES users
);

CREATE TABLE user_groups (
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups,
    PRIMARY KEY (user_id, group_id)
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('completed', 'in_progress', 'not_started')) DEFAULT 'not_started',
    creator_id INTEGER REFERENCES users,
    assignee_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups,
    parent_task_id INTEGER REFERENCES tasks,
    deadline TIMESTAMP,
    time_to_complete INTERVAL
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    task_id INTEGER REFERENCES tasks,
    user_id INTEGER REFERENCES users
);

CREATE TABLE user_task_time (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    task_id INTEGER REFERENCES tasks,
    time_spent INTERVAL,
    logged_at TIMESTAMP DEFAULT NOW()
);