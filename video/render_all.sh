#!/usr/bin/env bash
# usage: ./render_all.sh S1 S3 S5 ...   renders each session at 720p30 with Kokoro narration, then builds out/ files
cd "$(dirname "$0")"
mkdir -p logs
for N in "$@"; do
  mod=$(echo $N | tr 'S' 's')
  echo "=== $N start $(date +%T)"
  .venv/bin/manim -qm --disable_caching $mod.py $N > logs/render_$N.log 2>&1 && ./build.sh $N 720p30 >> logs/render_$N.log 2>&1 \
    && echo "=== $N done $(date +%T)" || echo "=== $N FAILED $(date +%T) (see logs/render_$N.log)"
done
