@ECHO OFF

REM Crear usuario y base de datos
psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -c "CREATE DATABASE siniestros;" -W
