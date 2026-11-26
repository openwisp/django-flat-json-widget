#!/bin/bash
# Install the selected Django and CI dependencies in separate review phases.
set -e
if [ "${CI_SYSTEM_DEPS_READY:-0}" != 1 ]; then
    sudo npm install -g prettier
fi
if [ "${CI_SYSTEM_DEPS_ONLY:-0}" = 1 ]; then
    exit 0
fi
python -m pip install -U pip wheel setuptools
python -m pip install -U -e ".[test]"
python -m pip install -U "${DJANGO_VERSION:?Set DJANGO_VERSION to a CI matrix value}"
