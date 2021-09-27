#!/usr/bin/env python3
import subprocess
import sys
import json
from pprint import pprint

gcolor = "--gtest_color=yes"
gtest_args = [gcolor]
exe = "enter here"

failed_indicator = "[  FAILED  ] "
passed_indicator = "[  PASSED  ] "
summary_indicator = "[==========] "
failed_tests_file_name = "failed_tests.json"
test_suit_separator = "] \x1b[m"

all_failing_flag = "--run_all_failing"
failing_flag = "--run_failing"

def run_tests(tests = dict(), override_failing_storage = True):
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
    output = dict()
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
            output[str(indicator_count)] = test_str
            count += 1
        else:
            print(pl)

    if override_failing_storage :
        f = open(failed_tests_file_name, "w")
        f.write(json.dumps(output))
        f.close()

def run_all_tests():
    run_tests()

def run_failed_tests():
    with open(failed_tests_file_name) as f:
        data = json.load(f)
    run_tests(data,False)

def run_specific_failed_tests(tests):
    with open(failed_tests_file_name) as f:
        data = json.load(f)
    filter_tests = dict()
    for test in tests:
        if test in data.keys():
            filter_tests[test] = data[test]
    if len(filter_tests) == 0:
        run_failed_tests();
    else:
        run_tests(filter_tests,False )

def process_tests():
    if all_failing_flag in sys.argv:
        run_failed_tests()
    elif failing_flag in sys.argv:
        tests =sys.argv[sys.argv.index(failing_flag)+1:]
        run_specific_failed_tests(tests)
    else:
        run_all_tests()


process_tests()


