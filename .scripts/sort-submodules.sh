#!/usr/bin/sh
set -eu

dates=$(git submodule --quiet foreach --recursive sh -c "
  git log --date=iso \$(git rev-list --max-parents=0 HEAD) \
    | awk -F': ' '/Date/ {print \$2}' \
    | xargs -I'{}' date --date='{}' -Is --utc \
    | xargs -I'{}' printf '%s %s\n' {} \"\$(basename \"\${PWD}\")\"
")
printf '%s' "${dates}" | sort
