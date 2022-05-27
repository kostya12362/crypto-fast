-- upgrade --
ALTER TABLE "user" DROP COLUMN "phone";
-- downgrade --
ALTER TABLE "user" ADD "phone" VARCHAR(200);
