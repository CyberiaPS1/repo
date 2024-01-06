#!/bin/sh

if [ ! -f "$(git rev-parse --git-dir)/commit.template" ]; then
  echo "# [type of change]: [short description of change]" > "$(git rev-parse --git-dir)/commit.template"
  echo "#" >> "$(git rev-parse --git-dir)/commit.template"
  echo "# [longer description of change, optional]" >> "$(git rev-parse --git-dir)/commit.template"
  echo "# [any relevant context or background information, optional]" >> "$(git rev-parse --git-dir)/commit.template"
  echo "#" >> "$(git rev-parse --git-dir)/commit.template"
  echo "# [issue or ticket number, optional]" >> "$(git rev-parse --git-dir)/commit.template"
fi

