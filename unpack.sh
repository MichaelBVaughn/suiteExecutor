#!/bin/bash

tar -xvf tcasPackage.tar
cd tcasPackage
cd c-tools
make build-all
cd ..
cd reversePatcher
make
cd ..
cd time
make build
cd ..
cd tsl
make build
cd ..
cd tcas/scripts
./tcasExec.py

