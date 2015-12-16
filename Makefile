SRC_DIR=vimPackage
PACKAGE_NAME=vimPackage
PACKAGE_TAR=$(PACKAGE_NAME).tar
SCRIPT_DIR=vimPackage/vim/scripts
EXEC_SCRIPT_NAME=vimExec.py
TEST_DIR=/scratch/packageTest

all: package

test: package
	cp $(PACKAGE_NAME) $(TEST_DIR); \
	cd $(TEST_DIR); \
	./unpack.sh 42

package: suiteExecutor execScript unpackScript
	tar -cvf $(PACKAGE_TAR) $(SRC_DIR)

suiteExecutor:
	cp suiteExecutor.py $(SCRIPT_DIR)

execScript:
	cp $(EXEC_SCRIPT_NAME) $(SCRIPT_DIR)

shebangFix:
	cp shebangFix $(SCRIPT_DIR)

unpackScript:
	cp unpack.sh $(TEST_DIR)
