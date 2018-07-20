CREATE TABLE client (
	account varchar(255) NOT NULL UNIQUE,
	username varchar(255) NOT NULL,
	password varchar(20) NOT NULL,
	PRIMARY KEY (account)
);

CREATE TABLE photo (
	id serial NOT NULL,
	date_p date NOT NULL,
	description text NOT NULL,
	client_p varchar(255) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (client_p) REFERENCES client(account)
);

CREATE TABLE followers (
	followed varchar(255) NOT NULL,
	follower varchar(255) NOT NULL,
	FOREIGN KEY (follower) REFERENCES client(account),
	FOREIGN KEY (followed) REFERENCES client(account)
);

CREATE TABLE comment (
	id serial NOT NULL,
	date_c date NOT NULL,
	comment varchar(255) NOT NULL,
	id_photo integer NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_photo) REFERENCES photo(id)
);

CREATE TABLE lik (
	id integer NOT NULL,
	u_user varchar(255) NOT NULL,
	photo integer NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (u_user) REFERENCES client(account),
	FOREIGN KEY (photo) REFERENCES photo(id)
);
