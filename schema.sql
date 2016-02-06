#Define how the data base is set up

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  food text not null,
  attributes text
);

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  email text not null,
  KeyWords text
);