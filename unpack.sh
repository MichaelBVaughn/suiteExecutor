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
./tcasExec.py $1
cd ../..
diff tcas/source/tcas.c tcas/versions.alt/versions.orig/v41/tcas.c  >> "job-$1-result.txt" 
