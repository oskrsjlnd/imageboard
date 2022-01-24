CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    role TEXT,
    password TEXT,
    username TEXT UNIQUE
);
