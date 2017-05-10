#!/usr/bin/env python3

import os
import json
from glob import glob
import pprint
import datetime
import dateutil.parser
import csv

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.getcwd(), 'data'))


def find_release_files():
    for file in glob(os.path.join(DATA_DIR, '*/*')):
        yield file


if __name__ == '__main__':

    csvdata = list()

    for filename in find_release_files():
        with open(filename, 'r') as f:
            graph = json.load(f)

        # pprint.pprint(graph)
        # break

        for task in graph['tasks']:
            # pprint.pprint(task)
            taskid = task['status']['taskId']
            provisionerid = task['task']['provisionerId']
            workertype = task['task']['workerType']
            dependencies = task['task']['dependencies']
            for run in task['status']['runs']:
                # print(run)

                # if run['state'] != 'completed':
                #	continue
                if run['state'] in ['exception', 'pending']:
                    continue
                scheduled_time = dateutil.parser.parse(run['scheduled'])
                start_time = dateutil.parser.parse(run['started'])
                end_time = dateutil.parser.parse(run['resolved'])

                duration = end_time - start_time
                delay = start_time - scheduled_time
                print("Duration: {}, delay: {}".format(duration, delay))

                csvdata.append([taskid, provisionerid, workertype, scheduled_time,
                                start_time, end_time, duration, delay])

    with open('rundata1.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for line in csvdata:
            writer.writerow(line)

        # link to, under task:
        # provisionerId
        # workerType
        # status -> workerType
        # Tree:
        # status -> taskId
        # dependencies
        # pprint.pprint(graph['tasks'][0]['status']['runs'])
