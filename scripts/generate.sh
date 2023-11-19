#!/bin/bash

COUNT=20

echo Generating $COUNT

for ((i=1; i<=COUNT; i++)); do
  text="todo$i"
  curl -X 'POST' \
  'http://localhost:8000/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "title=$text"
done
