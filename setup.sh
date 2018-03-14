#!/usr/bin/env bash

apt-get install python-setuptools python-dev build-essential 
easy_install pip
pip install numpy scipy

# setup environment variable
echo "export PYTHONPATH=$PYTHONPATH:$(pwd)/src" >> ~/.profile
echo "export SOCIALSIMPATH=$(pwd)" >> ~/.profile

# setup pre-commit hook
cp ./script/hook/pre-commit ./.git/hooks
