DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS watched;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE wishlist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  movietitle TEXT NOT NULL,
  posterPath TEXT NOT NULL,
  voteCount INTEGER,
  overview TEXT,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE watched (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  movietitle TEXT NOT NULL,
  posterPath TEXT NOT NULL,
  voteCount INTEGER,
  overview TEXT,
  upvoteCount INTEGER DEFAULT 0,
  downvoteCount INTEGER DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

