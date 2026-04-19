#!/usr/bin/env bash

cat test_snapshot.csv \
  | python mappers/sort-by-month.py \
  | python mappers/speaker-name-mapper.py \
  | python mappers/unit-name-mapper.py \
  > final_schedule.csv