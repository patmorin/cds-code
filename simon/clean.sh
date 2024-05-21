#/usr/bin/env bash

echo "Running dev tools..."

code=src/*

echo "Running Black:"
black $code

echo "Running Isort:"
isort $code

echo "Running Flake8:"
flake8 $code