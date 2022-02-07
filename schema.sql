DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    admin BOOLEAN,
    password TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE
);
