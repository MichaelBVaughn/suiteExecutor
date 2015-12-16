#!/bin/bash

wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/x-tools.tar.gz
tar -xvzf x-tools.tar.gz
rm x-tools.tar.gz

wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/tcl.tar.gz
tar -xvzf tcl.tar.gz
rm tcl.tar.gz


wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/vim_1.0.tar
tar -xvf vim_1.0.tar
rm vim_1.0.tar

#TCL/expect installs aren't relocatable. Luckily they build in ~1 minute.
export CC=$_CONDOR_JOB_IWD/x-tools/x86_64-unknown-linux-gnu/x86_64-unknown-linux-gnu-gcc

wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/tcl8.5.18-src.tar.gz
tar -xvzf tcl8.5.18-src.tar.gz
rm tcl8.5.18-src.tar.gz

wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/expect5.45.tar.gz
tar -xvzf expect5.45.tar.gz
rm expect5.45.tar.gz

mkdir tcl
mkdir expect

cd tcl8.5.18/unix/
./configure --prefix=$_CONDOR_JOB_IWD/tcl
make
make install
cd ../..

cd expect5.45
./configure --with-tcl=$_CONDOR_JOB_IWD/tcl8.5.18/unix --with-tclinclude=$_CONDOR_JOB_IWD/tcl8.5.18/generic
make
make install
cd ..

export PATH=$_CONDOR_JOB_IWD/tcl/bin
#Finish installing tcl/expect

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
