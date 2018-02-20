#!/bin/bash

for f in $(find ${SOCIALSIMPATH} -name '*.py'); do yapf --style google -i $f; done
