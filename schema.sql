CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    leader_id INTEGER REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE UserGroups (
    user_id INTEGER REFERENCES Users ON DELETE CASCADE,
    group_id INTEGER REFERENCES Groups ON DELETE CASCADE,
    PRIMARY KEY (user_id, group_id)
);

CREATE TABLE Tasks (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT,
    creator_id INTEGER REFERENCES Users ON DELETE CASCADE,
    assignee_id INTEGER REFERENCES Users ON DELETE CASCADE,
    group_id INTEGER REFERENCES Groups ON DELETE CASCADE,
    deadline DATE
);

CREATE TABLE TaskTime (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    task_id INTEGER REFERENCES Tasks,
    time_spent INTERVAL,
    assigned_at TIMESTAMP DEFAULT NOW()
);