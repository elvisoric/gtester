#!/usr/bin/env python3
import subprocess
import sys
import json
from pprint import pprint
from pathlib import Path

gcolor = "--gtest_color=yes"
gtest_args = [gcolor]
exe = ""

failed_indicator = "[  FAILED  ] "
passed_indicator = "[  PASSED  ] "
summary_indicator = "[==========] "
config_path_prefix = Path(".gtester")
config_name = "config.json"
config_path_prefix.mkdir(exist_ok = True)
config_path = (config_path_prefix / config_name)

test_suit_separator = "] \x1b[m"

failing_flag = "--run_failing"
exe_flag = "--exe"

def run_tests(tests = dict(), override_failing_storage = True):
    if len(exe) == 0:
        print("Please provide exe using --exe");
        return
    check_for_failed = True
    tag_test = False
    skip_first_failed_tag = True
    if len(tests) == 0:
        gtest_filter = "*"
    else:
        gtest_filter = ":".join(tests.values())

    gtest_args.append('--gtest_filter=' + gtest_filter)
    args = [exe] + gtest_args
    popen = subprocess.Popen(" ".join(args), shell = True,stdout=subprocess.PIPE, universal_newlines=True)
    tests_output = dict()
    count = 1
    for line in popen.stdout:
        pl = line[:-1]
        if passed_indicator in pl:
            check_for_failed = False
        if summary_indicator in pl:
            tag_test = True
            print(pl)
        if tag_test and not check_for_failed and failed_indicator in pl:
            p = pl.find(test_suit_separator)
            test_str = pl[p + len(test_suit_separator) :]
            if skip_first_failed_tag:
                skip_first_failed_tag = False
                print(pl)
                continue
            if gtest_filter == "*":
                indicator_count = count
            else:
                for k, v in tests.items():
                    if test_str == v:
                        indicator_count = k
                        break

            indicator = '\33[91m' +'[' + str(indicator_count) + '] ' + '\033[0m'

            print(pl + " " + indicator)
            tests_output[str(indicator_count)] = test_str
            count += 1
        else:
            print(pl)

    if override_failing_storage :
        output = dict();
        output['exe'] = exe
        output['tests'] = tests_output
        f = open(config_path, "w")
        f.write(json.dumps(output))
        f.close()

def run_all_tests():
    global exe
    if config_path.exists():
        with open(config_path) as f:
            config_data = json.load(f)
        exe = config_data['exe']
    run_tests()

def run_failed_tests():
    with open(config_path) as f:
        config_data = json.load(f)
    exe = config_data['exe']
    tests = config_data['tests']
    run_tests(tests,False)

def run_specific_failed_tests(tests):
    global exe
    with open(config_path) as f:
        config_data = json.load(f)
    exe = config_data['exe']
    data = config_data['tests']
    filter_tests = dict()
    for test in tests:
        if test in data.keys():
            filter_tests[test] = data[test]
    if len(filter_tests) == 0:
        run_failed_tests();
    else:
        run_tests(filter_tests,False )

def process_tests():
    if exe_flag in sys.argv:
        exe = sys.argv[sys.argv.index(exe_flag) + 1]
        output = dict();
        output['exe'] = exe
        output['tests'] = dict()
        f = open(config_path, "w")
        f.write(json.dumps(output))
        f.close()
    elif failing_flag in sys.argv:
        tests =sys.argv[sys.argv.index(failing_flag)+1:]
        run_specific_failed_tests(tests)
    else:
        run_all_tests()


process_tests()


