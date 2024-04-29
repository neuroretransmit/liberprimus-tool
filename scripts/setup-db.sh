#!/bin/sh

cat db/sql/ddl.sql | sqlite3 solution_attempts.db

