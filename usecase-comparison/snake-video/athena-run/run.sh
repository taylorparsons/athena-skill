#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

METRICS_FILE="game-metrics.json"
VALIDATION_FILE="validation-report.json"
VIDEO_FILE="artifacts/video.mp4"
mkdir -p docs

run_start_utc="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
run_start_epoch="$(date -u +%s)"

cleanup() {
    local exit_code="${1:-0}"
    local status="DONE"
    local ended_utc="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    local ended_epoch="$(date -u +%s)"
    local duration=$((ended_epoch - run_start_epoch))

    if [ "$exit_code" -ne 0 ]; then
        status="FAILED"
    fi

    {
        printf 'Run Metadata\n'
        printf 'action: athena\n'
        printf 'run_id: athena\n'
        printf 'started_utc: %s\n' "$run_start_utc"
        printf 'ended_utc: %s\n' "$ended_utc"
        printf 'start_epoch: %s\n' "$run_start_epoch"
        printf 'end_epoch: %s\n' "$ended_epoch"
        printf 'duration_seconds: %s\n' "$duration" 
        printf 'status: %s\n' "$status" 
    } > docs/run-metadata.md

    exit "$exit_code"
}

trap 'cleanup $?' EXIT

mkdir -p artifacts

python3 src/snake_game.py --output "$METRICS_FILE" "$@"
python3 src/validate_snake_game.py "$METRICS_FILE" | tee "$VALIDATION_FILE"
python3 src/render_snake_video.py "$METRICS_FILE" --out artifacts --video "$VIDEO_FILE"

printf 'Run complete. Artifacts: %s, %s, %s\n' "$METRICS_FILE" "$VALIDATION_FILE" "$VIDEO_FILE"
