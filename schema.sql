DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS image;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS subject;

CREATE TABLE user(
    id SERIAL PRIMARY KEY,
    admin BOOLEAN,
    password TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE
);

CREATE TABLE image(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user,
    subject_id INTEGER REFERENCES subject,
    name TEXT,
    ts_timezone TIMESTAMPTZ,
    data BYTEA
);

CREATE TABLE imglike(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user,
    image_id INTEGER REFERENCES image
);

CREATE TABLE comment(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user,
    image_id INTEGER REFERENCES image,
    content TEXT
); 

CREATE TABLE subject(
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE cmntlike(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user,
    comment_id INTEGER REFERENCES comment
);