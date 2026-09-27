#!/usr/bin/env bash
# SessionStart hook: install Python packages in Claude Code cloud sessions only.
# Always exits 0 so a failed install never blocks the session from starting.
if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  cd "$(dirname "$0")/.." || exit 0
  echo "[install_pkgs] cloud session detected: installing requirements.txt"
  pip install --quiet --disable-pip-version-check -r requirements.txt \
    || echo "[install_pkgs] WARNING: pip install failed (is PyPI allowed in the network settings?)"
fi
exit 0
