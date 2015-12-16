SRC_DIR=tcasPackage
PACKAGE_NAME=tcasPackage
PACKAGE_TAR=$(PACKAGE_NAME).tar
SCRIPT_DIR=tcasPackage/tcas/scripts
EXEC_SCRIPT_NAME=tcasExec.py
TEST_DIR=/u/v/a/vaughn/packageTest

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

unpackScript:
	cp unpack.sh $(TEST_DIR)
