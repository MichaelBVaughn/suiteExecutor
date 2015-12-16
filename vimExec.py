#!/usr/bin/python
import os
import sys
import suiteExecutor

def make_trial_result_filename(job_num, trial_num):
    return "job-" + str(job_num) + "-trial-" + str(trial_num) + "-results.txt"

def write_mutins_info(info, dest_file):
    dest_file.write("MUTANT INFO+" + str(len(info)) + "\n")
    dest_file.writelines(info)

def attempt_compile_and_record(util, out_file):
    result = util.compile_at_compile_dir()
    if 0 == result:
        out_file.write("compilation succeeded\n")
    else:
        out_file.write("compilation failed\n")
    return result
        
#mutate until successful compilation, or attempts exceeds tries
#requires the verbose mutator
def iter_mut_and_compile(util, job, tries, output_dir, test_script_name):
    outFile = None
    seed_offset = job * tries
    for i in range(job, job + tries):
        if outFile is not None:
            outFile.close()            
        outFilename = make_trial_result_filename(job, i)
        outFilePath = os.path.join(output_dir, outFilename)
        outFile = open(outFilePath)
        cur_seed = seed_offset + i
        result = util.mutate_at_compile_dir(seed=cur_seed)
        (dot_orig, dot_c, patch_txt) = suiteExecutor.deconstruct_verbose_results(result)
        write_mutins_info(patch_txt, outFile)
        if attempt_compile_and_record(util, outFile):
            util.run_test_script(test_script_name)
            break

            
        
job_num = sys.argv[1]
tries = sys.argv[2]
exp_root = os.path.abspath("../..")
name = "tcas"
test_name = "universe"
script_name = "runall-diff.sh"
mutator_path = os.path.join(exp_root, "reversePatcher/bin/mutins")
db_path = os.path.join(exp_root, "reversePatcher/mutants.dat")

mutator = suiteExecutor.VerboseRandPatchMutator(mutator_path, db_path)
util = suiteExecutor.SIRUtil(exp_root, name, 41, test_name, SiemensTests = True, mutator = mutator)

util.move_version_to_compile_dir()
iter_mut_and_compile(util, job_num, tries, exp_root, script_name)
#TODO: add comp_path once everything else works. Then, package original test results at path.
#TODO: look at old-style test building
#util.make_test_script_at_build(test_name, script_name)


