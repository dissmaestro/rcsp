#!/bin/bash

COUNT=${1:-10}

# generate one todo
echo Generating $COUNT

text="asdas"

curl -X 'POST' \
  'http://localhost:8000/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "task=$text"
