#!/usr/bin/env bash
set -euo pipefail

: "${AWX_URL:?AWX_URL is required}"
: "${AWX_TOKEN:?AWX_TOKEN is required}"
: "${AWX_JOB_TEMPLATE_ID:?AWX_JOB_TEMPLATE_ID is required}"

python3 scripts/trigger_awx.py
