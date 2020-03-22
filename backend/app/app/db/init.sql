CREATE TABLE IF NOT EXISTS "user"
(
    id         serial            NOT NULL
        CONSTRAINT user_pk
            PRIMARY KEY,
    first_name varchar(50)       NOT NULL,
    last_name  varchar(50)       NOT NULL,
    email      varchar(100)      NOT NULL,
    sso_token  varchar(100),
    type       integer DEFAULT 0 NOT NULL,
    course_id  varchar(10)
);

ALTER TABLE "user"
    OWNER TO "user";

CREATE UNIQUE INDEX IF NOT EXISTS user_email_uindex
    ON "user" (email);

CREATE TABLE IF NOT EXISTS sport
(
    id   serial      NOT NULL
        CONSTRAINT sport_pk
            PRIMARY KEY,
    name varchar(50) NOT NULL
);

ALTER TABLE sport
    OWNER TO "user";

CREATE TABLE IF NOT EXISTS "group"
(
    id         serial      NOT NULL
        CONSTRAINT group_pk
            PRIMARY KEY,
    name       varchar(50) NOT NULL,
    sport_id   integer
        CONSTRAINT group_sport_id_fk
            REFERENCES sport
            ON UPDATE CASCADE ON DELETE SET NULL,
    trainer_id integer
        CONSTRAINT group_user_id_fk
            REFERENCES "user"
            ON UPDATE CASCADE ON DELETE SET NULL
);

ALTER TABLE "group"
    OWNER TO "user";

CREATE TABLE IF NOT EXISTS quiz
(
    id        serial NOT NULL
        CONSTRAINT quiz_pk
            PRIMARY KEY,
    author_id integer
        CONSTRAINT quiz_user_id_fk
            REFERENCES "user"
            ON UPDATE CASCADE ON DELETE SET NULL,
    created   timestamp DEFAULT now(),
    active    boolean   DEFAULT TRUE
);

ALTER TABLE quiz
    OWNER TO "user";

CREATE TABLE IF NOT EXISTS selected_priority
(
    user_id  integer NOT NULL
        CONSTRAINT selected_priority_user_id_fk
            REFERENCES "user"
            ON UPDATE CASCADE ON DELETE CASCADE,
    group_id integer NOT NULL
        CONSTRAINT selected_priority_group_id_fk
            REFERENCES "group"
            ON UPDATE CASCADE ON DELETE CASCADE,
    priority integer NOT NULL,
    quiz_id  integer NOT NULL
        CONSTRAINT selected_priority_quiz_id_fk
            REFERENCES quiz
            ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT selected_priority_pk
        UNIQUE (user_id, group_id, quiz_id)
);

ALTER TABLE selected_priority
    OWNER TO "user";

