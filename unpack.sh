#!/bin/bash

wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/x-tools.tar.gz
tar -xvzf x-tools.tar.gz
rm x-tools.tar.gz

#set the permissions so I can install everything
find x-tools -name "*" | xargs chmod 777

wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/vimPackageTest.tar
tar -xvf vimPackageTest.tar
rm vimPackageTest.tar

#TCL/expect installs aren't relocatable. Luckily they build in ~1 minute.
export CC=$_CONDOR_JOB_IWD/x-tools/x86_64-unknown-linux-gnu/bin/x86_64-unknown-linux-gnu-gcc
export _CROSS_COMPILER_SYSROOT=$_CONDOR_JOB_IWD/x-tools/x86_64-unknown-linux-gnu/x86_64-unknown-linux-gnu/sysroot
wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/tcl8.5.18-src.tar.gz
tar -xvzf tcl8.5.18-src.tar.gz
rm tcl8.5.18-src.tar.gz

wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/expect5.45.tar.gz
tar -xvzf expect5.45.tar.gz
rm expect5.45.tar.gz

cd tcl8.5.18/unix/
./configure --prefix=$_CROSS_COMPILER_SYSROOT
make
make install
cd ../..

cd expect5.45
./configure --with-tcl=$_CONDOR_JOB_IWD/tcl8.5.18/unix --with-tclinclude=$_CONDOR_JOB_IWD/tcl8.5.18/generic
make
make install
cd ..

export PATH=$_CROSS_COMPILER_SYSROOT/bin:$PATH
#Finish installing tcl/expect

#Build ncurses so that we can build vim
wget http://proxy.chtc.wisc.edu/SQUID/mvaughn/ncurses-5.9.tar.gz
tar -xvzf ncurses-5.9.tar.gz
rm ncurses-5.9.tar.gz

cd ncurses-5.9
./configure --with-build-cc=$CC --prefix=$_CROSS_COMPILER_SYSROOT
make
make install
cd ..

export PATH=$_CONDOR_JOB_IWD/x-tools/x86_64-unknown-linux-gnu/bin:$PATH

cd vimPackage
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
cd vim/scripts
./vimExec.py $1 $2
cd ../..

