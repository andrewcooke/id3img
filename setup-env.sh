#!/bin/bash

rm -fr env
virtualenv-3.4 --python=python3.4 env
source env/bin/activate
easy_install nose

