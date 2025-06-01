Conectar ao PostgreSQL:

psql -U postgres (assumindo o super user postgres)



Criar Postgres DB:

CREATE DATABASE <db_name>;



Criar Postgres User:

CREATE USER <username> WITH PASSWORD <'yourpassword'> SUPERUSER;



Conectar à DB:

psql -U <username> -d <db_name>



Correr scripts SQL:

psql -U <username> -d <db_name> -f <script.sql>