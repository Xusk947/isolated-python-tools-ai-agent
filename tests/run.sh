#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TESTS_DIR="${ROOT_DIR}/tests"
OUT_DIR="${TESTS_DIR}/outputs"
IMAGE_TAG="croki-python-sandbox-test:local"

mkdir -p "${OUT_DIR}"

docker build -t "${IMAGE_TAG}" "${ROOT_DIR}"

docker run --rm \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  --tmpfs /workspace:rw,nosuid,nodev,size=256m \
  -e HOME=/workspace \
  -e XDG_CONFIG_HOME=/workspace/.config \
  -e XDG_CACHE_HOME=/workspace/.cache \
  -e MPLBACKEND=Agg \
  -e MPLCONFIGDIR=/workspace/.mplconfig \
  -v "${TESTS_DIR}:/app/tests:ro" \
  -v "${OUT_DIR}:/app/tests/outputs" \
  -w /app \
  "${IMAGE_TAG}" \
  python3 -m unittest discover -v -s /app/tests
