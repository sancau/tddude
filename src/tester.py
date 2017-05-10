# coding=utf-8
"""
Runs the test suite and parse it's stdout output
Returns data for passed / failed count, execution time and the log

TODO:

1. Returns only seconds component from time
   Behavior in case of time > 1 minute is unknown

2. Code can not handle 'skipped' in pytest output


"""
from collections import namedtuple

import subprocess

PytestOutput = namedtuple('PytestOutput', ['failed', 'passed', 'time', 'log'])
Time = namedtuple('Time', ['hours', 'minutes', 'seconds'])


def parse_failed_token(token):
    sp = token.split(' ')
    assert sp[-1] == 'failed'
    assert int(sp[-2])
    assert any([c == '=' for c in sp[0]])
    failed_count = int(sp[-2])
    return failed_count


def parse_passed_token(token):
    sp = token.split(' ')
    assert int(sp[0]) 
    assert sp[1] == 'passed'
    assert sp[2] == 'in'
    assert float(sp[3])
    assert sp[4] == 'seconds'
    passed_count = int(sp[0])
    return passed_count


def parse_time(token):
    # yet works for seconds only 
    sp = token.split(' ')
    assert float(sp[0]) 
    assert sp[1] in ['passed', 'failed']
    assert sp[2] == 'in'
    assert float(sp[3])
    assert sp[4] == 'seconds'
    hours = None
    minutes = None
    seconds = float(sp[3])
    return hours, minutes, seconds


def parse_second_token(token):
    sp = token.split(' ')
    assert any([c == '=' for c in sp[0]])
    assert int(sp[1]) 
    assert sp[2] in ['passed', 'failed']
    assert sp[3] == 'in'
    assert float(sp[4])
    assert sp[5] == 'seconds'
    assert any([c == '=' for c in sp[6]])
    hours = None
    minutes = None
    seconds = float(sp[4])
    passed_count = int(sp[1]) if sp[2] == 'passed' else 0
    failed_count = int(sp[1]) if sp[2] == 'failed' else 0    
    return passed_count, failed_count, hours, minutes, seconds


def parse_pytest_output(s):
    last = [i for i in s.split('\n') if i ][-1]  # last line of output

    splitted = last.split(', ')

    if len(splitted) == 2:
        # there are failed as well as passed
        failed = parse_failed_token(splitted[0])
        passed = parse_passed_token(splitted[1])
        hours, minutes, seconds = parse_time(splitted[1])
    elif len(splitted) == 1:
        # there are only failed or only passed
        passed, failed, hours, minutes, seconds = \
            parse_second_token(splitted[0])
    else:
        print(last)
        print(splitted)
        raise AssertionError('Can not recognize py.test output format')
        
    return PytestOutput(failed, passed, Time(hours, minutes, seconds), s)


def test(work_dir='.'):
    result = subprocess.run('pytest {}'.format(work_dir), stdout=subprocess.PIPE, shell=True)
    str_result = result.stdout.decode('utf-8')
    return parse_pytest_output(str_result)
