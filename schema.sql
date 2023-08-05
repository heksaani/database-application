CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    leader_id INTEGER REFERENCES Users
);

CREATE TABLE UserGroups (
    user_id INTEGER REFERENCES Users,
    group_id INTEGER REFERENCES Groups,
    PRIMARY KEY (user_id, group_id)
);

CREATE TABLE Tasks (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('completed', 'in progress', 'not started, late')) DEFAULT 'not started',
    creator_id INTEGER REFERENCES Users,
    assignee_id INTEGER REFERENCES Users,
    group_id INTEGER REFERENCES Groups,
    parent_task_id INTEGER REFERENCES Tasks,
    deadline TIMESTAMP,
    time_to_complete INTERVAL
);

CREATE TABLE Comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    task_id INTEGER REFERENCES Tasks,
    user_id INTEGER REFERENCES Users
);

CREATE TABLE TaskTime (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    task_id INTEGER REFERENCES Tasks,
    time_spent INTERVAL,
    logged_at TIMESTAMP DEFAULT NOW()
);