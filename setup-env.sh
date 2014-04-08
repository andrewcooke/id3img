#!/bin/bash

rm -fr env
virtualenv-3.3 --python=python3.3 env
source env/bin/activate
#easy_install stagger
easy_install nose

