#! /usr/bin/python

from testrail import *

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
    }
    ],
    'custom_throughput': None,
    'defects': None,
    'elapsed': None,
    'status_id': 8,
    'version': None
}


class Base():

    def __init__(self):
        self.client = APIClient('https://mirantis.testrail.com')
        self.client.user = '.com'
        self.client.password = ''

    def get_plans(self, project_id):
        return self.client.send_get('get_plans/{0}'.format(project_id))

    def get_plan(self, plan_id):
        return self.client.send_get('get_plan/{0}'.format(plan_id))

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

    def get_test_results_for_run(self, run_id):
        return self.client.send_get('get_results_for_run/{0}'.format(run_id))

    def get_results_for_case(self, run_id, case_id):
        return self.client.send_get('get_results_for_case/{0}/{1}'.format(run_id, case_id))

    def get_test(self, test_id):
        return self.client.send_get('get_test/{0}'.format(test_id))

    def get_runs(self, run_id):
        return self.client.send_get('get_runs/{0}'.format(run_id))

    def get_run(self, run_id):
        return self.client.send_get('get_run/{0}'.format(run_id))

    def add_result(self,test_id , result_to_add):
        return self.client.send_post('add_result/{0}'.format(test_id['id']), result_to_add)

    def update_swift_cases(self, plan_id, result_to_add):
        tests = self.get_tests(plan_id)

        for i in tests:
            if i['status_id'] == 5 and 'tempest.api.object_storage' in i['custom_test_group']:
                print 'id: {0}  status_id: {1} name {2}'.format(i['id'], i['status_id'], i['custom_test_group']) #   status_id 1 - pass 5 - fail 8 - prod_fail
                result = self.add_result(i, result_to_add)
                print result

    def get_all_ids_tempest_runs_iso_90(self):
        runs = self.get_plans(3)
        tempest_runs = []
        for i in runs:
            if '9.0 iso #' in i['name']:
                if i['passed_count'] > 1000:
                    tempest_runs.append(i['id'])
                    # print i['name'], i['passed_count'], i['url']
        return tempest_runs

    def get_tempest_runs_in_iso(self, run_id):
        in_iso = self.get_plan(run_id)
        result = []
        for item in in_iso['entries']:
            # print item['runs'][0]['description']
            if item['runs'][0]['description']:
                if '[9.0][MOSQA] Tempest 9.0' in item['runs'][0]['description']:
                    # print item['runs'][0]
                    result.append(item['runs'][0])
        return result

    def find_tempest_iso_with_fialed_tests(self):
        run_ids = self.get_all_ids_tempest_runs_iso_90()
        run_ids.sort(reverse=True)
        iso = []
        for id in run_ids:
            results = self.get_tempest_runs_in_iso(id)
            for i in results:
                if i.has_key('failed_count'):
                    if i['failed_count'] > 0:
                        iso.append(i['id'])
                        # print i['id']
        return iso



if __name__ == '__main__':
    call = Base()
    # print call.get_plans(3)
    # print call.get_tests(8904)
    # tr = call.get_tempest_runs(8873)
    # ids = call.get_id_of_tempest_runs(tr)
    # call.get_tests(ids[0])
    # test_ids = call.get_id_of_failed_tests(ids[0])
    # print call.get_test_result(4608631)
    # print call.get_results_for_case(8904, 16871)
    # print call.get_test(4608631)
    # print call.get_runs(3)
    # call.update_swift_cases(9047, add_result)
    # print call.find_tempest_iso_with_fialed_tests()
    res = call.get_test_results_for_run(9047)
    for i in res:
        if i['status_id'] == 5:
            print i

