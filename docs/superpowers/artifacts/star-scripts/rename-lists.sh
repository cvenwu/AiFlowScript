#!/usr/bin/env bash
# 重命名可复用的旧列表 -> 目标分类。recipe: open -> Edit list -> fill Name -> focus+Enter
set -uo pipefail
# slug<TAB>新名称
RENAMES=(
  "algorithm	算法"
  "interview	面试 / 八股"
  "systemdesign	分布式 / 系统设计"
  "softskills	软技能 / 职业"
  "c	C / C++"
  "devops	云原生 / DevOps"
  "tools	工具 / 效率"
)
for row in "${RENAMES[@]}"; do
  slug="${row%%	*}"; newname="${row##*	}"
  echo "=== $slug -> $newname ==="
  agent-browser open "https://github.com/stars/cvenwu/lists/$slug" >/dev/null 2>&1
  sleep 1.8
  agent-browser find text "Edit list" click >/dev/null 2>&1
  sleep 1.8
  NAME=$(agent-browser snapshot 2>&1 | grep -iE 'textbox "Name"' | grep -oE 'e[0-9]+' | head -1)
  [ -z "$NAME" ] && { echo "  ! no name field, skip"; continue; }
  agent-browser fill "@$NAME" "$newname" >/dev/null 2>&1
  sleep 0.6
  VAL=$(agent-browser get value "@$NAME" 2>&1 | head -1)
  agent-browser focus "@$NAME" >/dev/null 2>&1
  agent-browser press "Enter" >/dev/null 2>&1
  sleep 2
  echo "  filled=[$VAL] submitted"
done
echo "ALL DONE"
