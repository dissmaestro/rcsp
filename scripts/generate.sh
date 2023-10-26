#!/bin/bash

for i in {1..20}
do
curl -X 'POST' \
  'http://localhost:8000/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "task=todo-$i"
done
