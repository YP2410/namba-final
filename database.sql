

/*
    This table is for all users - we use the chat_ID for a unique identifier for each user.
    We use text because we got "int out of index" with the chat_ID's.
*/
CREATE TABLE users (
                         user_ID text NOT NULL,
                         PRIMARY KEY (user_ID)
);

/*
    In this table we just save the admins data
*/
CREATE TABLE admins (
                       Username text NOT NULL,
                       Password int NOT NULL,
                       PRIMARY KEY (Username)
);


/*
    In this table we save the general data of the polls.
    We save the number of answers of each possible answer (answers_counter).
    poll_ID - we use the poll id (long) given by the bot API, we convert it to text for convenience reasons.
*/
CREATE TABLE polls (
                       poll_ID text NOT NULL,
                       question text NOT NULL,
                       answers text[] NOT NULL,
                       answers_counter int[] NOT NULL,
                       closed boolean NOT NULL,
                       multiple_choice bool NOT NULL,
                       quiz boolean NOT NULL,
                       correct_answers int[],
                       solution text,
                       PRIMARY KEY (poll_ID)
);



/*
    This table stores the answers per user for a specific poll.
    This table allows us to make sure that a user can't vote twice (and more) for the same poll
    and also check who are the users who voted a specific answer at a given poll.
*/
CREATE TABLE polls_answers (
                       poll_ID text NOT NULL,
                       user_ID text NOT NULL,
                       answers text[] NOT NULL,
                       is_correct boolean NOT NULL,
                       PRIMARY KEY (poll_ID, user_ID),
                       FOREIGN KEY (poll_ID) references polls on delete cascade,
                       FOREIGN KEY (user_ID) references users on delete cascade
);