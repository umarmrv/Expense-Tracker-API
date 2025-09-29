-- Создаём пользователя exp_user, если его нет
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'exp_user'
   ) THEN
      CREATE ROLE exp_user WITH LOGIN PASSWORD 'exp_pass';
   END IF;
END
$$;

-- Пытаемся создать базу (на чистом старте создастся, при повторном запуске выдаст WARNING)
CREATE DATABASE expense_db OWNER exp_user;

-- Даём все права пользователю exp_user
GRANT ALL PRIVILEGES ON DATABASE expense_db TO exp_user;
