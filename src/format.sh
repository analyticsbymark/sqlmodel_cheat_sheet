#!/bin/sh -e
set -x

"C:\Users\markc\Documents\GitHub\sql_cheat_sheet\Scripts\autoflake.exe" --remove-all-unused-imports --recursive --remove-unused-variables --in-place . --exclude=__init__.py
"C:\Users\markc\Documents\GitHub\sql_cheat_sheet\Scripts\black.exe" .
"C:\Users\markc\Documents\GitHub\sql_cheat_sheet\Scripts\isort.exe" .
sleep 5