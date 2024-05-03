#!/bin/sh

if ! command -v black; then
  pip install black
fi

black $(find . -path ./venv -prune -o -name "**.py")
