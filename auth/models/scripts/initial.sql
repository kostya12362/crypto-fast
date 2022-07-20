CREATE OR REPLACE FUNCTION select_user_auth_rows(
    email_new character varying = NULL,
    provider_new character varying = NULL,
    id_provide_new character varying = NULL
)
    RETURNS TABLE (
                    id            integer,
                    user_id       integer,
                    username      character varying,
                    provider      character varying,
                    id_provide    character varying,
                    email         character varying
                  )
    LANGUAGE sql
AS
$func$
WITH user_auth_select as (
    select * from user_auth as ua2
    WHERE ua2.email = email_new
          AND ua2.provider = provider_new
          AND ua2.id_provide = id_provide_new
)
SELECT id, user_id, username, provider, id_provide, email FROM user_auth_select;
$func$;

-- select * from select_user_auth_rows(email_new := 'rota1998f4f104@gmail.com', provider_new := 'email', id_provide_new := '124rfdsfsdg234234');

CREATE OR REPLACE FUNCTION create_user_row(
    email_new character varying = NULL,
    provider_new character varying = NULL,
    id_provide_new character varying = NULL,
    username_new character varying = NULL,
    password_hash_new character varying = NULL
)
    RETURNS TABLE
            (
                user_id       integer,
                phone         character varying,
                date_joined   timestamp with time zone,
                general_email character varying,
                is_verified   boolean,
                username      character varying,
                provider      character varying,
                id_provide    character varying,
                email         character varying,
                anti_phishing bool,
                email_active  int[],
                otp_active    int[],
                phone_active  int[]
            )
    LANGUAGE plpgsql
AS
$func$
DECLARE
    new_user_id int;
    _rec record;
    count_rows_user_auth int;
BEGIN
    SELECT * FROM select_user_auth_rows(email_new, provider_new, id_provide_new) INTO _rec;
    SELECT count(*) FROM select_user_auth_rows(email_new, provider_new, id_provide_new) INTO count_rows_user_auth;
    RAISE notice '%', _rec;
    IF count_rows_user_auth > 1 THEN
        RAISE 'Detect many rows in "user_auth"';
    END IF;
    IF count_rows_user_auth = 0 THEN
        IF provider_new not in ('email', 'google', 'facebook', 'telegram') THEN
            RAISE 'Not detect provider';
        END IF;
        IF provider_new = 'email' and (email_new is null or password_hash_new is null) THEN
            RAISE 'Provide type "email" using with field "password" and "email" ';
        END IF;
        IF provider_new in ('facebook', 'google', 'telegram') and id_provide_new is null  THEN
            RAISE 'Provide type "facebook" and "google" using with field "id_provide"';
        END IF;
        IF provider_new = 'email' THEN
            INSERT INTO "user" (general_email) VALUES (email_new) RETURNING id INTO new_user_id;
        ELSE
            INSERT INTO "user" (date_joined, is_verified) VALUES (NOW(), true) RETURNING id INTO new_user_id;
            INSERT INTO "security" (user_id) VALUES (new_user_id);
        END IF;
        INSERT INTO "user_auth" (provider, id_provide, email, user_id, username, password_hash)
        VALUES (provider_new, id_provide_new, email_new, new_user_id, username_new, password_hash_new);
        RETURN QUERY
            SELECT ua.user_id,
                   u.phone,
                   u.date_joined,
                   u.general_email,
                   u.is_verified,
                   ua.username,
                   ua.provider,
                   ua.id_provide,
                   ua.email,
                   s.anti_phishing,
                   s.email_active,
                   s.otp_active,
                   s.phone_active
            FROM select_user_auth_rows(email_new, provider_new, id_provide_new) AS ua
                     JOIN "user" u ON u.id = ua.user_id
                     JOIN "security" s on u.id = s.user_id;
    ELSE
        IF provider_new = 'telegram' and _rec.username != username_new THEN
            UPDATE "user_auth" as ua3
            SET username = username_new
            WHERE ua3.id = _rec.id;
            raise notice 'Value: % %', _rec.username, username_new;
        END IF;
        RETURN QUERY
            SELECT ua.user_id,
                   u.phone,
                   u.date_joined,
                   u.general_email,
                   u.is_verified,
                   ua.username,
                   ua.provider,
                   ua.id_provide,
                   ua.email,
                   s.anti_phishing,
                   s.email_active,
                   s.otp_active,
                   s.phone_active
            FROM select_user_auth_rows(email_new, provider_new, id_provide_new) AS ua
                     JOIN "user" u ON u.id = ua.user_id
                     JOIN "security" s on u.id = s.user_id;
    END IF;
END
$func$;





CREATE OR REPLACE FUNCTION email_verification_and_join_table(j_user_id int)
    RETURNS table(id int, email varchar, phone varchar, date_joined timestamp with time zone, is_verified bool, otp_active int[], phone_active int[], anti_phishing bool)
as
$update$
    UPDATE "user" iw
    SET    is_verified = true
    where id = j_user_id;
    select u.id, u.general_email, u.phone, u.date_joined, u.is_verified, s.otp_active, s.phone_active, s.anti_phishing from "user" as u
    join "security" s on u.id = s.user_id
    where u.id = j_user_id
    limit 1;
$update$
    LANGUAGE sql;


-- GET ALL data user login history
CREATE OR REPLACE FUNCTION select_history_login(j_user_id int)
    RETURNS table(system varchar, detail json)
    LANGUAGE sql;
AS
$select$
select
       nullif(concat(hl.browser, ' V'), '') || nullif(concat(hl.version, ''), '') || ' (' || hl.os_system || ')' as system,
       array_to_json(array_agg(json_build_object(
           'id', hl.id,
           'last_login', hl.last_login,
           'location', nullif(concat(hl.country, ', '), '') || nullif(hl.city, ''),
           'ip_address', hl.ip_address,
           'session_id', hl.session) order by hl.last_login desc )) as detail
from history_login as hl
join security s on s.id = hl.security_id
where s.user_id = j_user_id

GROUP by system

order by system desc;
$select$;
-- END

-- IF CREATE user_auth provider email not create row in security table
-- AFTER update verify account create new row

CREATE OR REPLACE FUNCTION create_security_row() RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$func$
BEGIN
    INSERT INTO "security" ("user_id") VALUES (NEW.id)
    ON CONFLICT DO NOTHING;
    RETURN new;
END;
$func$;

DROP TRIGGER IF EXISTS trigger_security_insert_
  ON "user";
CREATE TRIGGER trigger_security_insert_
    BEFORE UPDATE of is_verified ON "user"
    FOR EACH ROW
    EXECUTE PROCEDURE create_security_row();
--END

