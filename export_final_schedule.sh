#!/usr/bin/env bash

cat "${1:-/dev/stdin}" \
  | python mappers/sort-by-month.py \
  | python mappers/speaker-name-mapper.py \
  | python mappers/unit-name-mapper.py \
  > final_schedule.csv