#! /usr/bin/python

from testrail import *

class Base():

    def __init__(self):
        self.client = APIClient('https://mirantis.testrail.com')
        self.client.user = 'sturivnyi@mirantis.com'
        self.client.password = 'asr5znW0tq!'

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

    def get_plans(self, plans_id):
        return self.client.send_get('get_plan/{0}'.format(plans_id))

    def get_tests(self, plan_id):
        return self.client.send_get('get_tests/{0}'.format(plan_id))

    def get_tempest_runs(self, plan_id):
        all_run = self.get_plans(plan_id)
        tempest_runs = []
        for run in all_run['entries']:
            if 'Tempest 9.0' in run['name']:
                tempest_runs.append(run)
        return tempest_runs

    def get_id_of_tempest_runs(self, tempest_runs):
        tempest_runs_ids = []
        for i in tempest_runs:
            for item in i['runs']:
                tempest_runs_ids.append(item['id'])
        return tempest_runs_ids

    def get_id_of_failed_tests(self, tempest_run_id):
        all_tests = self.get_tests(tempest_run_id)
        test_ids = []
        for test in all_tests:
            if test['status_id'] == 5:
                test_ids.append(test['id'])
        return test_ids

    def get_test_result(self, test_id):
        return self.client.send_get('get_results/{0}'.format(test_id))

    def get_results_for_case(self, run_id, case_id):
        return self.client.send_get('get_results_for_case/{0}/{1}'.format(run_id, case_id))

    def get_test(self, test_id):
        return self.client.send_get('get_test/{0}'.format(test_id))

    def get_runs(self, run_id):
        return self.client.send_get('get_runs/{0}'.format(run_id))

# for i in tests:
#     if i['status_id'] == 5 and 'tempest.api.object_storage' in i['custom_test_group']:
#         print 'id: {0}  status_id: {1} name {2}'.format(i['id'], i['status_id'], i['custom_test_group']) #   status_id 1 - pass 5 - fail 8 - prod_fail
#         result = client.send_post('add_result/{0}'.format(i['id']), add_result)
#         print result


#
#
# rs = client.send_post('add_result/4556564', add_result)
# print rs

if __name__ == '__main__':
    call = Base()
    # print call.get_plans(8873)
    # print call.get_tests(8904)
    # tr = call.get_tempest_runs(8873)
    # ids = call.get_id_of_tempest_runs(tr)
    # call.get_tests(ids[0])
    # test_ids = call.get_id_of_failed_tests(ids[0])
    # print call.get_test_result(4608631)
    # print call.get_results_for_case(8904, 16871)
    # print call.get_test(4608631)
    print call.get_runs(3)