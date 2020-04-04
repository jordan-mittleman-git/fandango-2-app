DROP TABLE IF EXISTS RegUser;
DROP TABLE IF EXISTS Theater;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS Seat;
DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS Time;
DROP TABLE IF EXISTS Schedule;
DROP TABLE IF EXISTS Listings;


CREATE TABLE RegUser (
   user_id varchar(255) NOT NULL PRIMARY KEY,
   name varchar(255) NOT NULL,
   email varchar(255) NOT NULL UNIQUE,
   phone int NOT NULL
);


CREATE TABLE Theater (
   address varchar(255) NOT NULL PRIMARY KEY,
   name varchar(255) NOT NULL
);


CREATE TABLE Room (
   number int NOT NULL,
   theater_addr varchar(255) NOT NULL,
   capacity int NOT NULL,
   PRIMARY KEY (number, theater_addr),
   FOREIGN KEY (theater_addr) REFERENCES Theater (address)
);


CREATE TABLE Seat (
   seat_number int NOT NULL, 
   room_number int NOT NULL,
   theater_addr varchar(255) NOT NULL,
   PRIMARY KEY (seat_number, room_number, theater_addr),
   FOREIGN KEY (room_number, theater_addr) REFERENCES Room (number, theater_addr)
);


CREATE TABLE Movie (
   movie_id varchar(255) NOT NULL PRIMARY KEY,
   name varchar(255) NOT NULL,
   genre varchar(255) NOT NULL,
   rating varchar(255) NOT NULL CHECK (rating IN ('G', 'PG', 'PG13', 'R', 'NC-17', 'Unrated'))
);


CREATE TABLE Time (
   time_slot varchar(255) NOT NULL CHECK (time_slot IN ('morning', 'afternoon', 'evening')),
   date date NOT NULL,
   PRIMARY KEY (time_slot, date)
);


CREATE TABLE Schedule (
   movie_id varchar(255) NOT NULL, 
   room_number int NOT NULL,
   theater_addr varchar(255) NOT NULL,
   time_slot varchar(255) NOT NULL,
   date date NOT NULL,
   ticket_price int NOT NULL,
   PRIMARY KEY (movie_id, time_slot, date, room_number, theater_addr),
   FOREIGN KEY (movie_id) REFERENCES Movie (movie_id),
   FOREIGN KEY (room_number, theater_addr) REFERENCES Room (number, theater_addr),
   FOREIGN KEY (time_slot, date) REFERENCES Time (time_slot, date)
);


CREATE TABLE Listings (
   user_id varchar(255),
   movie_id varchar(255) NOT NULL, 
   seat_number int NOT NULL,
   room_number int NOT NULL,
   theater_addr varchar(255) NOT NULL,
   time_slot varchar(255) NOT NULL,
   date date NOT NULL,
   ticket_price int NOT NULL,
   PRIMARY KEY (seat_number, room_number, theater_addr, time_slot, date),
   FOREIGN KEY (movie_id, time_slot, date, room_number, theater_addr, ticket_price) REFERENCES Schedule (movie_id, time_slot, date, room_number, theater_addr, ticket_price),
   FOREIGN KEY (user_id) REFERENCES RegUser (user_id),
   FOREIGN KEY (seat_number, room_number, theater_addr) REFERENCES Seat (seat_number, room_number, theater_addr)
);
