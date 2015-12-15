#!/bin/bash

wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/x-tools.tar.gz
tar -xvzf x-tools.tar.gz
rm x-tools.tar.gz

export PATH=$_CONDOR_JOB_IWD/x-tools/x86_64-unknown-linux-gnu/bin:$PATH

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
