#!/usr/bin/python3

import sys
import yaml


def list_module_names(mod_names):
    for n in mod_names:
        print(n, end=' ')


def generate_git_make(modules_list, git_op):
    print("T=", end='')
    for m in modules_list:
        print(m["module"], end=' ')
    print("\nall: $(T)\n.PHONY: all $(T)\n")

    for m in modules_list:
        mod_name = m["module"]
        mod = modules[mod_name]
        print(
            "%s:\n\t./git_%s_one.sh %s %s %s %s\n" %
            (mod_name, git_op, mod["url"], mod["remote"], m["from"], mod_name))


def generate_cmake(proj_modules,
                   proj_name,
                   proj_ver,
                   cmake_ver,
                   build_type="Release",
                   install_path="install",
                   single_tree=True):
    print("cmake_minimum_required(VERSION %s)\n" % (cmake_ver))
    print("project(%s VERSION %s)\n" % (proj_name, proj_ver))
    print("set(SINGLE_TREE %s)\n" % ("YES" if single_tree else "NO"))

    print("set(CMAKE_INSTALL_PREFIX %s)\n" % (install_path))
    print("set(CMAKE_PREFIX_PATH %s)\n" % (install_path))

    print("set(BUILD_TYPE %s)\n" % (build_type))
    print("set(BUILD_RUNNER_DIR build-runner/build-runner)\n")

    for m in proj_modules:
        if m["cmake"]:
            print("add_subdirectory(%s)" % (m["module"]))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = "help"

    if mode == "help":
        print("Usage: project.py sync | gen | push | list [all | cmake | develop]");
        print("  sync - pull by rebase all modules from their remotes");
        print("  gen - generate root cmake file for the project");
        print("  push - push all development modules to their remotes");
        print("  list all - list names of all modules");
        print("  list develop - list names of all develop-mode modules");
        print("  list cmake - list names of all modules buildable by cmake");
        sys.exit(0)

    manifest_fname = "manifest.yaml"

    with open(manifest_fname, "r") as file:
        manifest_root = yaml.load(file, Loader=yaml.FullLoader)

    # modules
    modules = manifest_root["modules"]

    # develop
    if 'develop' in manifest_root:
        develop_modules = manifest_root["develop"]
    else:
        develop_modules = []

    # consume
    if 'consume' in manifest_root:
        consume_modules = manifest_root["consume"]
    else:
        consume_modules = []

    # cmake
    cmake = manifest_root["cmake"]

    # project
    project = manifest_root["project"]

    proj_modules = develop_modules + consume_modules

    if mode == "sync":
        generate_git_make(proj_modules, "sync")
    elif mode == "push":
        generate_git_make(develop_modules, "push")
    elif mode == "gen":
        generate_cmake(proj_modules, project["name"], project["version"],
                       cmake["version"],
                       build_type=cmake["build"],
                       single_tree=cmake["single-tree"])
    elif mode == "list":
        if len(sys.argv) > 2:
            list_mode = sys.argv[2]
        else:
            list_mode = "cmake"

        if list_mode == "cmake":
            list_module_names(
                [m["module"] for m in proj_modules if m["cmake"]])
        elif list_mode == "develop":
            list_module_names([m["module"] for m in develop_modules])
        elif list_mode == "all":
            list_module_names([m["module"] for m in proj_modules])
    else:
        print("unexpected mode: %s\n" % (mode))
        sys.exit(1)
