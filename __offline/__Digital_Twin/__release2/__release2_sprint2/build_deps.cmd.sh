#!/usr/bin/env bash
set -eu

# Expecting to only build local dependencies of rather than the actual integrators and followers here.
DEPS=(
    rrps.dt.events
    rrps.dt.api.fielddata
)

pushd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)" > /dev/null

DIST_DIR=$(pwd)/dist

mkdir -p "$DIST_DIR"
for pkg in "${DEPS[@]}"; do
    echo -e "--------\nBuilding ${pkg}\n--------"
    pushd "$pkg" > /dev/null
    python3 setup.py -q check -mrs
    python3 setup.py -q sdist -d "$DIST_DIR"
    popd > /dev/null
done

popd > /dev/null
