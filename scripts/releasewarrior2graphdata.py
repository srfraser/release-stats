#!/usr/bin/env python3

import os
import json
from glob import glob
import taskcluster

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.getcwd(), 'data'))
RELEASES_DIR = os.environ.get('RELEASES_DIR')

ARCHIVE_DIR = os.path.join(RELEASES_DIR, 'ARCHIVE')

TC_CLIENT_ID = os.environ['TC_CLIENT_ID']
TC_ACCESS_TOKEN = os.environ['TC_ACCESS_TOKEN']


def find_release_files():
    file_pattern = '*.json'

    for path in RELEASES_DIR, ARCHIVE_DIR:
        for file in glob(os.path.join(path, file_pattern)):
            yield file


def examine_release_json(path):
    with open(path, 'r') as f:
        data = json.load(f)

    for build in data.get('builds'):
        if build.get('aborted', True) == True:
            continue
        if 'graphid' not in build or build['graphid'] == '':
            continue
        print(path, build.get('graphid'))
        return build.get('graphid')


def is_self_depending(task):
    return task['status']['taskId'] in task['task'].get('dependencies', list())


def sanitise_task_graph(taskgraph):
    # taskid = taskgraph['tasks'][0]['status']['taskId']
    # dependencies = taskgraph['tasks'][0]['task']['dependencies']
    sched_api = taskcluster.scheduler.Scheduler()

    print("Taskgraph has {} tasks".format(len(taskgraph['tasks'])))
    if not any(is_self_depending(task) for task in taskgraph['tasks']):
        return taskgraph

    scheduler_graph = sched_api.inspect(taskgraph['taskGroupId'])
    # print(scheduler_graph)
    scheduler_dict = {task['taskId']: task for task in scheduler_graph['tasks']}

    for task in taskgraph['tasks']:
        print("{}, replacing {} with {}".format(task['status']['taskId'], task['task'][
              'dependencies'], scheduler_dict.get(task['status']['taskId'], {}).get('requires', [])))
        task['task']['dependencies'] = scheduler_dict.get(
            task['status']['taskId'], {}).get('requires', [])

    return taskgraph


if __name__ == '__main__':
    index = taskcluster.Index(
        {'credentials': {'clientId': TC_CLIENT_ID, 'accessToken': TC_ACCESS_TOKEN}})
    index.ping()
    api = taskcluster.Queue()

    for filename in find_release_files():
        graphid = examine_release_json(filename)
        if not graphid:
            # print("Graph {} in {} is None".format(graphid, filename))
            continue
        # typo in graph id, at least once.
        graphid = graphid.rstrip('/')
        release = os.path.split(filename)[1].strip('.json')
        store_path = os.path.join(DATA_DIR, release)
        os.makedirs(store_path, exist_ok=True)

        if os.path.exists(os.path.join(store_path, graphid)):
            # already processed, we must be re-running
            continue

        print(graphid)
        taskgraph = api.listTaskGroup(graphid)
        taskgraph = sanitise_task_graph(taskgraph)

        with open(os.path.join(store_path, graphid), 'w') as f:
            f.write(json.dumps(taskgraph))
