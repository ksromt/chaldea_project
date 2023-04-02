DROP DATABASE IF EXISTS chaldea_test;
DROP USER IF EXISTS kirisaki;

CREATE DATABASE chaldea_test;
CREATE USER kirisaki WITH PASSWORD 'hxllxyly';
ALTER ROLE kirisaki SET client_encoding TO 'utf8';
ALTER ROLE kirisaki SET default_transaction_isolation TO 'read committed';
ALTER ROLE kirisaki SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE chaldea_test TO kirisaki;