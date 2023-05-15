#!/bin/bash
cd $(dirname $0)
cd /workspaces/ext-list

tox

if [ $? -ne 0 ]; then
    echo "pytest failed"
    exit 1
fi

python setup.py sdist
python setup.py bdist_wheel
twine upload --repository pypi dist/*
