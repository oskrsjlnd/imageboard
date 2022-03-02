DROP TABLE IF EXISTS "users" CASCADE;
DROP TABLE IF EXISTS "subject" CASCADE;
DROP TABLE IF EXISTS "image" CASCADE;
DROP TABLE IF EXISTS "imglike";
DROP TABLE IF EXISTS "comment" CASCADE;
DROP TABLE IF EXISTS "cmntlike";

CREATE TABLE "users"(
    user_id SERIAL PRIMARY KEY,
    admin BOOLEAN,
    password TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE
);

CREATE TABLE "subject"(
    subject_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE "image"(
    image_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "users" (user_id) ON DELETE CASCADE,
    subject_name TEXT REFERENCES "subject" (name),
    name TEXT,
    timezone TIMESTAMP,
    data BYTEA
);

CREATE TABLE "imglike"(
    imglike_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "users" (user_id) ON DELETE CASCADE,
    image_id INTEGER REFERENCES "image" (image_id) ON DELETE CASCADE
);

CREATE TABLE "comment"(
    comment_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "users" (user_id) ON DELETE CASCADE,
    image_id INTEGER REFERENCES "image" (image_id) ON DELETE CASCADE,
    content TEXT,
    time TIMESTAMP
); 

CREATE TABLE "cmntlike"(
    cmntlike_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "users" (user_id) ON DELETE CASCADE,
    comment_id INTEGER REFERENCES "comment" (comment_id) ON DELETE CASCADE
);