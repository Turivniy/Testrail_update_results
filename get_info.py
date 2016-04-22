#! /usr/bin/python

from testrail import *

client = APIClient('https://mirantis.testrail.com')
client.user = '@.com'
client.password = ''

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


tests = client.send_get('get_tests/8788') # plan id
# print 'test:', tests[44]

for i in tests:
    if i['status_id'] == 5 and 'tempest.api.object_storage' in i['custom_test_group']:
        print 'id: {0}  status_id: {1} name {2}'.format(i['id'], i['status_id'], i['custom_test_group']) #   status_id 1 - pass 5 - fail 8 - prod_fail
        result = client.send_post('add_result/{0}'.format(i['id']), add_result)
        print result





#
#
# rs = client.send_post('add_result/4556564', add_result)
# print rs
