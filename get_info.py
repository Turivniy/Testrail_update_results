#! /usr/bin/python

from testrail import *
from config import USER
from config import PASS

client = APIClient('https://mirantis.testrail.com')
client.user = USER
client.password = PASS

## Add result ======================

add_result = {
     'assignedto_id': None,
     'comment': None,
  'custom_baseline_stdev': None,
  'custom_baseline_throughput': None,
  'custom_launchpad_bug': 'https://bugs.launchpad.net/mos/+bug/1442193',
  'custom_stdev': None,
  'custom_test_case_steps_results': [{
      'actual':  '',
      'content': '',
      'expected': ''
  }],
  'custom_throughput': None,
  'defects': None,
  'elapsed': None,
  'status_id': 8,
  'version': None
}


class GetFailedTests:
    def __init__(self, plan_id):
        self.plan_id = plan_id

    def get_plan(self):
        return client.send_get('get_plan/{}'.format(self.plan_id))

    def get_suites(self):
        plan = self.get_plan()
        all_suites_ids = []
        for s in plan['entries']:
            all_suites_ids.append(s['runs'][0]['id'])
        return all_suites_ids

    def get_tests_results_by_suite(self, suite_id):
        return client.send_get('get_tests/{}'.format(suite_id))

    def get_all_tests_results(self):
        all_suites = self.get_suites()

        all_tests = []
        for suite in all_suites:
            test_results = self.get_tests_results_by_suite(suite)
            all_tests.append(test_results)

        return all_tests

    def get_failed_tests(self):
        # test['status_id'] == 5 failed test
        # test['status_id'] == 9 test failed
        all_tests_in_all_suites = self.get_all_tests_results()

        failed_tests = []
        for tests_in_suite in all_tests_in_all_suites:
            for test in tests_in_suite:
                if test['status_id'] == 9:
                    failed_tests.append(test)

        return failed_tests


tests = GetFailedTests('51082')
print(len(tests.get_failed_tests()))
