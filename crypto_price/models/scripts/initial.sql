CREATE OR REPLACE FUNCTION select_user_auth_rows(
    provider_new character varying,
    user_auth_new jsonb
)
    RETURNS TABLE
            (
                id            int,
                user_auth     jsonb,
                phone character varying,
                date_joined  timestamp with time zone,
                general_email character varying,
                is_verified bool,
                anti_phishing bool,
                email_active  int[],
                otp_active    int[],
                phone_active  int[]
            )
    LANGUAGE sql
AS
$func$
WITH user_auth_select AS (
    SELECT u.id,
           u.user_auth,
           u.phone,
           u.date_joined,
           u.general_email,
           u.is_verified,
           s.anti_phishing,
           s.email_active,
           s.otp_active,
           s.phone_active
    FROM "user" as u
             join "security" s on u.id = s.user_id
    WHERE u.user_auth -> provider_new ->> 'id' = user_auth_new ->> 'id'
       OR u.user_auth -> provider_new ->> 'email' = user_auth_new ->> 'email'
)
SELECT u1.id,
       u1.user_auth,
       u1.phone,
       u1.date_joined,
       u1.general_email,
       u1.is_verified,
       u1.anti_phishing,
       u1.email_active,
       u1.otp_active,
       u1.phone_active
FROM user_auth_select as u1;
$func$;

CREATE OR REPLACE FUNCTION create_user(
    user_auth_new jsonb,
    provider_new character varying = NULL
)

    RETURNS TABLE
            (
                id            integer,
                user_auth     jsonb,
                phone         character varying,
                date_joined   timestamp with time zone,
                general_email character varying,
                is_verified   boolean,
                anti_phishing bool,
                email_active  int[],
                otp_active    int[],
                phone_active  int[]
            )
    LANGUAGE plpgsql
AS
$func$
DECLARE
    _is_verify     bool default false;
    _general_email character varying default null;
    _rec           record;
    _rec_count     int;
BEGIN
    SELECT su.id
    INTO _rec
    FROM select_user_auth_rows(provider_new := provider_new, user_auth_new := user_auth_new) AS su;
    GET DIAGNOSTICS _rec_count = ROW_COUNT;
    IF _rec_count = 0 THEN
        IF provider_new IN ('email') THEN
            _general_email = user_auth_new ->> 'email';
        ELSE
            _is_verify = true;
        END IF;
        INSERT INTO "user" (user_auth, is_verified, general_email)
        VALUES (jsonb_build_object(provider_new, user_auth_new), _is_verify, _general_email)
        RETURNING * INTO _rec;
    ELSIF _rec_count = 1 AND provider_new IN ('telegram', 'google', 'facebook') THEN
        UPDATE "user" AS u1
        SET user_auth = jsonb_set(u1.user_auth, ARRAY [format('%s', provider_new)], user_auth_new, true)
        WHERE u1.id = _rec.id;
    ELSE
        raise 'using alreade';
    end if;
    RETURN QUERY (select "user".id,
                         "user".user_auth,
                         "user".phone,
                         "user".date_joined,
                         "user".general_email,
                         "user".is_verified,
                         s.anti_phishing,
                         s.email_active,
                         s.otp_active,
                         s.phone_active
                  from "user"
                           join security s on "user".id = s.user_id
                  where "user".id = _rec.id);
END
$func$;



CREATE OR REPLACE FUNCTION select_user_auth_rows_by_user_id(
    _user_id int
)
    RETURNS TABLE
            (
                id            int,
                user_auth     jsonb,
                phone character varying,
                date_joined  timestamp with time zone,
                general_email character varying,
                is_verified bool,
                anti_phishing bool,
                email_active  int[],
                otp_active    int[],
                phone_active  int[]
            )
    LANGUAGE sql
AS
$func$
WITH user_auth_select AS (
    SELECT u.id,
           u.user_auth,
           u.phone,
           u.date_joined,
           u.general_email,
           u.is_verified,
           s.anti_phishing,
           s.email_active,
           s.otp_active,
           s.phone_active
    FROM "user" as u
             join "security" s on u.id = s.user_id
    WHERE u.id = _user_id
)
SELECT u1.id,
       u1.user_auth,
       u1.phone,
       u1.date_joined,
       u1.general_email,
       u1.is_verified,
       u1.anti_phishing,
       u1.email_active,
       u1.otp_active,
       u1.phone_active
FROM user_auth_select as u1;
$func$;






CREATE OR REPLACE FUNCTION create_security_row_after() RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$func$
BEGIN
    INSERT INTO "security" ("user_id") VALUES (NEW.id)
    ON CONFLICT DO NOTHING;
    RETURN new;
END;
$func$;

DROP TRIGGER IF EXISTS trigger_security_insert_after
  ON "user";
CREATE TRIGGER trigger_security_insert_after
    AFTER INSERT ON "user"
    FOR EACH ROW
    EXECUTE PROCEDURE create_security_row_after();