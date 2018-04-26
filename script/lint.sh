#!/bin/bash

PY_FILES="$(find $SOCIALSIMPATH -type f -name "*.py")"

# pylint -E --rcfile=${SOCIALSIMPATH}/lint/pylint.rc ${PY_FILES}
pylint  ${PY_FILES}
