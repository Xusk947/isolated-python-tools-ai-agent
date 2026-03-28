#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TESTS_DIR="${ROOT_DIR}/tests"
OUT_DIR="${TESTS_DIR}/outputs"
IMAGE_TAG="croki-python-sandbox-test:local"

mkdir -p "${OUT_DIR}"

docker build -t "${IMAGE_TAG}" "${ROOT_DIR}"

docker run --rm \
  -v "${TESTS_DIR}:/app/tests:ro" \
  -v "${OUT_DIR}:/app/tests/outputs" \
  -w /app \
  "${IMAGE_TAG}" \
  python3 -m unittest discover -v -s /app/tests

