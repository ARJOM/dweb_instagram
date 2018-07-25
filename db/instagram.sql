CREATE TABLE client (
	account varchar(255) NOT NULL,
	username varchar(255) NOT NULL UNIQUE,
	password varchar(20) NOT NULL,
	PRIMARY KEY (username)
);

CREATE TABLE photo (
	id serial,
	date_p date NOT NULL,
	description text,
	client_p varchar(255),
	way text NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (client_p) REFERENCES client(username)
);

CREATE TABLE followers (
	followed varchar(255),
	follower varchar(255),
	FOREIGN KEY (follower) REFERENCES client(username),
	FOREIGN KEY (followed) REFERENCES client(username)
);

CREATE TABLE comment (
	id serial,
	date_c date NOT NULL,
	comment varchar(255) NOT NULL,
	id_photo integer NOT NULL,
	username VARCHAR(30) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_photo) REFERENCES photo(id),
	FOREIGN KEY (username) REFERENCES client(username)
);

CREATE TABLE lik (
	id serial,
	u_user varchar(255),
	photo integer,
	PRIMARY KEY (id),
	FOREIGN KEY (u_user) REFERENCES client(username),
	FOREIGN KEY (photo) REFERENCES photo(id)
);

