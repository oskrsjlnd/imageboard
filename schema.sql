DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS "subject" CASCADE;
DROP TABLE IF EXISTS "image" CASCADE;
DROP TABLE IF EXISTS "imglike";
DROP TABLE IF EXISTS "comment" CASCADE;
DROP TABLE IF EXISTS "cmntlike";

CREATE TABLE "user"(
    id SERIAL PRIMARY KEY,
    admin BOOLEAN,
    password TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE
);

CREATE TABLE "subject"(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE "image"(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user" (id),
    subject_name TEXT REFERENCES "subject" (name),
    name TEXT,
    timezone TIMESTAMP,
    data BYTEA
);

CREATE TABLE "imglike"(
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES "user" (id),
    image_id INTEGER REFERENCES "image" (id)
);

CREATE TABLE "comment"(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user" (id),
    image_id INTEGER REFERENCES "image" (id),
    content TEXT
); 

CREATE TABLE "cmntlike"(
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES "user" (id),
    comment_id INTEGER REFERENCES "comment" (id)
);