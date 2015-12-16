#!/usr/bin/python
import os
import sys
import suiteExecutor


#mutate until successful compilation, or attempts exceeds tries
#requires the verbose mutator
def iter_mut_and_compile(util, base, tries):
    for i in range(base, base + tries):
        result = util.mutate_at_compile_dir()
job_num = sys.argv[1]
exp_root = os.path.abspath("../..")
name = "tcas"
test_name = "universe"
script_name = "runall.sh"
mutator_path = os.path.join(exp_root, "reversePatcher/bin/mutins")
db_path = os.path.join(exp_root, "reversePatcher/mutants.dat")

mutator = suiteExecutor.PatchMutator(mutator_path, db_path)
util = suiteExecutor.SIRUtil(exp_root, name, 41, test_name, SiemensTests = True, mutator = mutator)

util.move_version_to_compile_dir()
util.mutate_at_compile_dir()
#TODO: add comp_path once everything else works. Then, package original test results at path.
#TODO: look at old-style test building
#util.make_test_script_at_build(test_name, script_name)
outFilename = "job-" + str(job_num) + "-result.txt"
outPath = os.path.join(exp_root, outFilename)
outFile = open(outPath, 'w')
if 0 == util.compile_at_compile_dir():
    outFile.write("compilation succeeded\n")
    util.run_test_script(script_name)
else:
    outFile.write("compilation failed\n")
