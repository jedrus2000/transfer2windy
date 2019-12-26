#!/usr/bin/env bash
rm -rf package/*
pip install -r requirements.txt --target ./package
mkdir -p package/transfer2windy
cp transfer2windy/* package/transfer2windy/
cd ./package
zip -9r ../transfer2windy.zip *
cd ..
