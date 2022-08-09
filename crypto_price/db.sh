#!/bin/bash
aerich init -t models.__init__.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade

#cat ./models/scripts/initial.sql | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"