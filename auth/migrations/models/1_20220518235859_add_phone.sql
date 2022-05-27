-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(200) NOT NULL UNIQUE,
    "phone" VARCHAR(200),
    "is_verified" BOOL NOT NULL  DEFAULT True
);
-- downgrade --
DROP TABLE IF EXISTS "user";
