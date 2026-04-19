#!/usr/bin/env bash

cat possible-solution-4.csv \
  | python mappers/sort-by-month.py \
  | python mappers/speaker-name-mapper.py \
  | python mappers/month-name-mapper.py \
  | python mappers/unit-name-mapper.py \
  > final_schedule.csv