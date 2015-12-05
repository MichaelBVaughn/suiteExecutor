#!/usr/bin/python
import os
import suiteExecutor

exp_root = os.path.abspath("../..")
name = "tcas"
test_name = "universe"
script_name = "runall2.sh"
mutator_path = os.path.join(exp_root, "reversePatcher/bin/mutins")
db_path = os.path.join(exp_root, "reversePatcher/mutants.dat")

mutator = suiteExecutor.PatchMutator(mutator_path, db_path)
util = suiteExecutor.SIRUtil(exp_root, name, 41, test_name, SiemensTests = True, mutator = mutator)

util.move_version_to_compile_dir()
util.mutate_at_compile_dir()
#TODO: add comp_path once everything else works. Then, package original test results at path.
util.make_test_script_at_build(test_name, script_name)
util.run_test_script(script_name)

