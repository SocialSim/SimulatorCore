#!/usr/bin/env bash

# setup environment variable
echo "export PYTHONPATH=$PYTHONPATH:$(pwd)/src" >> ~/.profile
echo "export SOCIALSIMPATH=$(pwd)" >> ~/.profile

# setup pre-commit hook
cp ./script/hook/pre-commit ./.git/hooks
