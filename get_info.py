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
        # test['status_id'] == 5 failed
        # test['status_id'] == 9 test failed
        # test['status_id'] == 10 infra failed
        all_tests_in_all_suites = self.get_all_tests_results()

        failed_tests = []
        for tests_in_suite in all_tests_in_all_suites:
            for test in tests_in_suite:
                if test['status_id'] == 5:
                    failed_tests.append(test)

        return failed_tests

    def get_test(self, test_id):
        return client.send_get('get_test/{}'.format(test_id))

    def get_test_result(self, test_id):
        test = self.get_test(test_id)
        return client.send_get('get_results_for_case/{}/{}'.format(test['run_id'], test['case_id']))

    def generate_link_on_failed_test(self, tests_ids):
        all_tests = []
        for t_id in tests_ids:
            all_tests.append('https://mirantis.testrail.com/index.php?/tests/view/{}'.format(t_id))

        for test in all_tests:
            print(test)
        return all_tests

    def get_failed_tests_results(self):
        failed_tests = self.get_failed_tests()
        test_results = []
        for test in failed_tests:
            test_results.append(
                client.send_get('get_results_for_case/{}/{}'.format(test['run_id'], test['case_id'])))
        return test_results

    def get_failed_infra_tests(self):
        failed_tests = self.get_failed_tests()
        # https://mirantis.jira.com/wiki/spaces/OSCORE/pages/1190856164/DevCloud+Infra+Issues
        INFRA_FAILED_TESTS = ['id-cc54ca6e-b91d-4ddd-80cc-24a886dfaaa0',
                              'id-3f7726fc-a41b-40ca-ab38-51e2973f146a',
                              'id-8da0f6cc-60e6-4298-9e54-e1f905c5552a',
                              'id-3d753d42-7c16-4a0e-8f73-875881826626']
        test_for_update = []
        for i_test in INFRA_FAILED_TESTS:
            for test in failed_tests:
                if i_test in test['title']:
                    test_for_update.append(test)
                    print('https://mirantis.testrail.com/index.php?/tests/view/{}'.format(test['id']))
        return test_for_update

    def update_failed_infra_tests(self):
        tests_for_update = self.get_failed_infra_tests()

        # test['status_id'] == 10 infra failed
        add_result = {
            'status_id': '10',
            'defects': 'PROD-22993',
            'comment': None,
            'elapsed': None,
            'version': None,
            'assignedto_id': None, }

        updated_test_results = []
        print("============= update_result =============")
        for test in tests_for_update:
            update_result = client.send_post('add_result/{}'.format(test['id']), add_result)
            updated_test_results.append(update_result)
            print(update_result['title'])
        return updated_test_results


if __name__ == '__main__':
    tests = GetFailedTests('51312')
    print(len(tests.get_failed_tests_results()))
