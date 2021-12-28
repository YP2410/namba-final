CREATE TABLE users (
                         Username varchar(255) NOT NULL,
                         PRIMARY KEY (Username)
);

CREATE TABLE admins (
                       Username varchar(255) NOT NULL,
                       Password int NOT NULL,
                       PRIMARY KEY (Username)
);