-- This will create a read only user, to be used by grafana
-- Since the database is not exposed we dont need a strong password

CREATE ROLE readaccess;
GRANT USAGE ON SCHEMA public TO readaccess;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readaccess;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readaccess;

CREATE USER grafana WITH PASSWORD 'grafana';
GRANT readaccess TO grafana;
