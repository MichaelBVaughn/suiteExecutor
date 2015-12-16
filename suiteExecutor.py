#!/usr/bin/python
import sys
import subprocess
import os
import shutil
import pdb
import shlex
    
class SIRUtil:
    #experiment root should be pulled from environment
    #name is the name of the subdirectory of experiment_root, containing the software object
    #version is the version number
    #SiemensTests should be set to true if the test directory structure is the classic style,
    #and false if there are subdirectories for versions.
    #mutator is some code that can be invoked to manipulate the code.
    #the name of the test framework to use.
    def __init__(self, experiment_root, name, version, test_name, SiemensTests = False, mutator = None): 
        self.mutator = mutator
        
        self.experiment_root = experiment_root
        self.obj_name = name
        self.version_num = version
        self.test_name = test_name
        #goofy, yeah.
        self.versions_dir = "versions.alt"
        self.orig_dir = "versions.orig"
        self.compilation_dir = "source"
        self.tests_dir = "testplans.alt"
        self.scripts_dir = "scripts"
        self.object_path = os.path.join(self.experiment_root, self.obj_name)
        self.scripts_path = os.path.join(self.object_path, self.scripts_dir)
        os.chdir(self.scripts_path)
        
        self.orig_versions_path = os.path.join(self.object_path, self.versions_dir, self.orig_dir)
        self.version_dir = "v" + str(self.version_num)
        self.version_src_path = os.path.join(self.orig_versions_path, self.version_dir)
        self.compilation_path = os.path.join(self.object_path, self.compilation_dir)

        self.tests_path = os.path.join(self.object_path, self.tests_dir)
        
        if(SiemensTests):
            self.version_tests_path = self.tests_path
        else:
            self.version_tests_path = os.path.join(self.tests_path, self.version_dir)

        self.outputs_dir = "outputs"
        self.outputs_alt_dir = "outputs.alt"
        self.outputs_path = os.path.join(self.experiment_root, self.outputs_dir)
        self.outputs_alt_path = os.path.join(self.experiment_root, self.outputs_alt_dir)
        self.outputs_alt_ver_path = os.path.join(self.outputs_alt_path, self.version_dir)

    def move_version_to_compile_dir(self):
        self.move_contents_to_dir(self.version_src_path, self.compilation_path)
        
    #dst_dir should exist first
    def move_contents_to_dir(self, src_dir, dst_dir):
        for (src_item_path, item_name) in self.abs_path_subdir_iter(src_dir):
            dst = os.path.join(dst_dir, item_name)
            self.copy_fs_item(src_item_path, dst)

    def copy_fs_item(self, src_path, dest_path):
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
        else:
            shutil.copyfile(src_path, dest_path)
        
    def abs_path_subdir_iter(self, dirname):
        for entry in os.listdir(dirname):
            yield (os.path.join(dirname, entry), entry)

    def compile_with_make(self, source_code_path):
        origin_dir = os.getcwd()
        os.chdir(source_code_path)
        exit_code = subprocess.call(["make","build"])
        os.chdir(origin_dir)
        return exit_code
        
    def compile_with_make_at_compile_dir(self):
        return self.compile_with_make(self.compilation_path)

    #works with classic Siemens programs
    def compile(self, source_code_path, prog_name):
        origin_dir = os.getcwd()
        os.chdir(source_code_path)
        exit_code = subprocess.call(["gcc", "-o", prog_name + ".exe", prog_name + ".c"])
        os.chdir(origin_dir)
        return exit_code

    #return value dependent on mutator
    def compile_at_compile_dir(self):
        return self.compile(self.compilation_path, self.obj_name)

    #return value dependent on mutator
    def mutate(self, source_code_path):
        return self.mutator.mutate(source_code_path)

    def mutate_at_compile_dir(self):
        return self.mutate(self.compilation_path)

    #theoretically it should be refactored up a level. No biggie. We'll do that
    #when there's free time.
    #mutate until successful compilation, or attempts exceeds tries
    #requires the verbose mutator
    def iter_mut_and_compile(self, base, tries):
        for i in range(base, base + tries):
            mut_output = 

    #TODO: make diff scripts too
    #mts must be in your path, and so must cmp
    #build_path: wherever object was built
    #universe_filename: name of test universe file
    #script_name: desired name of script to be created from universe file
    #comp_path, if supplied causes make_test_script to generate a diff script, comparing results with those at comp_path.
    def make_test_script(self, build_path, universe_filename, script_name, comp_path = "NULL"):
        executable_path = os.path.join(build_path, self.obj_name + ".exe")
        univ_file_path = os.path.join(self.version_tests_path, universe_filename)
        script_type = "D"
        if comp_path == "NULL":
            script_type = "R"
        print script_type
        mts_path = os.path.join(self.experiment_root, "mts/bin/bsh/mts")
        subprocess.call([mts_path, self.object_path, executable_path, univ_file_path, script_type, script_name, comp_path, "NULL"])

    def make_test_script_at_build(self, universe_filename, script_name, comp_path = "NULL"):
        self.make_test_script(self.compilation_path, universe_filename, script_name, comp_path)

    def run_test_script(self, script_name):
        script_path = os.path.join(self.scripts_path, script_name)
        subprocess.call([script_path], shell=True)
    
    def move_test_results_to_version_res(self):
        self.move_contents_to_dir(self.outputs_path, self.outputs_alt_ver_path)

class PatchMutator:
    def __init__(self, mutator_path, patch_db_path):
        self.mutator_path = mutator_path
        self.patch_db_path = patch_db_path

    def mutate(self, target_path):
        dir_arg = target_path
        find_cmd = "find " + dir_arg + " -name \"*.c\""
        find_args = shlex.split(find_cmd)
        find_proc = subprocess.Popen(find_args, stdout = subprocess.PIPE)
        (find_stdout, find_stderr) = find_proc.communicate()
        mut_cmd = "xargs " + self.mutator_path + " -x " + self.patch_db_path + " -t"
        mut_args = shlex.split(mut_cmd)
        mut_proc = subprocess.Popen(mut_args, stdin = subprocess.PIPE)
        mut_proc.communicate(find_stdout)

class VerboseRandPatchMutator:
    def __init__(self, mutator_path, patch_db_path, seed):
        self.mutator_path = mutator_path
        self.patch_db_path = patch_db_path
        self.seed = seed

    #get C files, pipe them through xargs to mutator.
    #returns stdout from mutins -v as a string.
    def mutate(self, target_path):
        dir_arg = target_path
        find_cmd = "find " + dir_arg + " -name \"*.c\""
        find_args = shlex.split(find_cmd)
        find_proc = subprocess.Popen(find_args, stdout = subprocess.PIPE)
        mut_cmd = "xargs " + self.mutator_path + "-v -x " + self.patch_db_path + " -r " + str(self.seed) + " -t"
        mut_args = shlex.split(mut_cmd)
        mut_proc = subprocess.Popen(mut_args, stdin = find_proc.stdout, stdout = subprocess.PIPE)
        find_proc.stdout.close()
        output = mut_proc.communicate()[0]
        return output

#returns (.orig filename, .c filename, patch_data)
def deconstruct_verbose_results(result_str):
    lines = result_str.splitlines()
    name_line = lines[2] 
    dot_orig = lines[10:] #remove "Creating ./"
    dot_c = dot_orig[:-6] #remove ".orig."
    patch_data = lines[3:]
    return (dot_orig, dot_c, patch_data)    

