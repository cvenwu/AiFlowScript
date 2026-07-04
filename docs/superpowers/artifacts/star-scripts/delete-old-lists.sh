#!/usr/bin/env bash
# 删除 20 个不复用的旧 Star List。逐个：打开 -> Edit list -> Delete list -> 确认 Delete
set -uo pipefail
SLUGS=(
  "books"
  "java"
  "c-language"
  "%E4%BA%91%E5%8E%9F%E7%94%9F"
  "database"
  "design-pattern"
  "linux"
  "%E6%B8%B8%E6%88%8F%E5%BC%80%E5%8F%91"
  "os"
  "network"
  "resume"
  "iot"
  "cloud-computing"
  "assembly"
  "tsdb"
  "docker"
  "linux-kernel"
  "readme"
  "frontend"
)
for slug in "${SLUGS[@]}"; do
  echo "=== deleting $slug ==="
  agent-browser open "https://github.com/stars/cvenwu/lists/$slug" >/dev/null 2>&1
  sleep 1.5
  agent-browser find text "Edit list" click >/dev/null 2>&1
  sleep 1.5
  DEL=$(agent-browser snapshot 2>&1 | grep -iE 'button "Delete list"' | grep -oE 'e[0-9]+' | head -1)
  [ -z "$DEL" ] && { echo "  ! no Delete-list button, skip"; continue; }
  agent-browser click "@$DEL" >/dev/null 2>&1
  sleep 1.2
  CONF=$(agent-browser snapshot 2>&1 | grep -iE 'button "Delete"$|button "Delete" \[' | grep -oE 'e[0-9]+' | head -1)
  [ -z "$CONF" ] && { echo "  ! no confirm button, skip"; continue; }
  agent-browser click "@$CONF" >/dev/null 2>&1
  sleep 1.5
  echo "  done"
done
echo "ALL DONE"
