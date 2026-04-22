#!/usr/bin/env bash
# Build the Cytoscape.js viewer data for docs/graph/.
#
# Re-run whenever topics/**/*.yaml changes and a fresh interactive preview is
# needed. The output is a static JSON file checked in under docs/graph/ so the
# viewer can be opened directly via GitHub Pages or `python -m http.server`.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT="${REPO_ROOT}/docs/graph/graph.json"

mkdir -p "$(dirname "${OUTPUT}")"

python "${SCRIPT_DIR}/graph.py" \
  --repo-path "${REPO_ROOT}" \
  --format cytoscape \
  --output "${OUTPUT}"

echo "Graph JSON: ${OUTPUT}"
