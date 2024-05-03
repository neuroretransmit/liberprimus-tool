#!/bin/sh

docker kill liberprimus-tool_db_1
docker kill liberprimus-tool_adminer_1
docker-compose down --volumes
docker volume rm liberprimus-tool_db_data
