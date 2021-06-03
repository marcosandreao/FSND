#!/bin/bash
docker cp trivia.psql postgres:/ && docker exec -it postgres /bin/bash -c '
su - postgres bash -c "dropdb trivia_test"
su - postgres bash -c "createdb trivia_test"
psql -U postgres trivia_test < trivia.psql
'