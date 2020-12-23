create table if not exists users(
    id serial PRIMARY KEY,
    user_name varchar(255),
    password varchar(255),
    email varchar(255)
);

create table if not exists tags(
    id serial PRIMARY KEY,
    title varchar(255)
);

create table if not exists notes(
    id serial PRIMARY KEY,
    note_text text,
    owner_id bigint,
    title varchar(255),
    tag_id bigint,
    FOREIGN KEY (owner_id) REFERENCES users(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

create table if not exists edits(
    id serial PRIMARY KEY,
    editor_id bigint,
    note_id bigint,
    edit_timestamp timestamp
);

create table if not exists foreign_editors(
    id serial PRIMARY KEY,
    editor_id bigint,
    note_id bigint
);