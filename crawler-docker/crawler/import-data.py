#!/usr/bin/env python
#
# (c) Swirrl Ltd 2014
#
# Author: Rick Moynihan
#
# Upload the local rdf files to fuseki

import os
import sys
import glob
import time
import copy
import traceback

retry_limit = 10

retry_delays = [0,1,1,2,3,5,8,13,21,34]

class UploadFailure(StandardError):
    pass

def execute(command):
    print command
    return os.system(command)


def post_data(update_endpoint, rdf_file, delays):
    delays = copy.copy(delays)
    time.sleep(delays.pop(0))
    command = "curl -f -X POST -H \"Content-Type: application/rdf+xml\" -d @" + rdf_file + " " + update_endpoint
    posted = execute(command)

    while posted != 0:
        if not delays:
            raise UploadFailure('Failed to upload file after %s retries of command: %s ' %(len(retry_delays), command))
        time.sleep(delays.pop(0))
        print "retrying: " + command
        ret = os.system(command)

def is_initial_import():
    return len(sys.argv) >= 3 and sys.argv[2] == "initial_import"

def fetch_snapshot(update_endpoint, snapshot_name):
    if not is_initial_import():
        snapshot_file = "/tmp/" + snapshot_name + ".ttl"
        execute("curl -f -X GET -H \"Accept: application/turtle\" " + update_endpoint + " > " + snapshot_file)
    else:
        print "Initial import, not creating a snapshot"

def restore_snapshot(graph_endpoint, snapshot_name):
    if not is_initial_import():
        snapshot_file = "/tmp/" + snapshot_name + ".ttl"
        execute("curl -f -X POST -H \"Content-Type: application/turtle\" -d @" + snapshot_file + " " + graph_endpoint)
    else:
        print "This is the initial run so there is nothing to restore."

def start_transaction(end_point):
    print "TODO: implement start transaction... add a triple into a metadata graph that we check"

def end_transaction(end_point):
    print "TODO: implement end transaction... delete the metadata graph that we check"

def delete_graph(graph_endpoint):
    if not is_initial_import():
        execute("curl -f -X DELETE " + graph_endpoint)
    else:
        print "Ignoring removal of graph, as this is the initial run."

def import_rdf_files(base_path, graph_endpoint):
    rdf_files = glob.glob(base_path + "/*.rdf")

    # POST all rdf files in the directory to the triple store.
    for rdf_file in rdf_files:
        post_data(graph_endpoint, rdf_file, retry_delays)

def get_remote_data(dataset_name):
    command = None
    if dataset_name == "eldis":
        command = "/home/crawler/crawler/eldis/eldis_update.py"
    else:
        command = "/home/crawler/crawler/r4d/r4d_update.py"

    print "Fetching remote " + dataset_name + " data: " + command
    os.system(command)


def import_data(dataset_name, endpoint):
    graph_uri = "http://linked-development.org/" + dataset_name + "/"
    graph_endpoint = endpoint + "?graph=" + graph_uri
    base_path = "/home/" + dataset_name + "/rdf/"

    get_remote_data(dataset_name)

    fetch_snapshot(graph_endpoint, dataset_name)

    start_transaction(endpoint)
    delete_graph(graph_endpoint)
    try:
        import_rdf_files(base_path, graph_endpoint)
    except Exception, e:
        print "Failed to import data attempting to restore last working set..."
        print e
        print traceback.print_exc()
        restore_snapshot(graph_endpoint, dataset_name)

    end_transaction(end_point)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: import-data.py eldis|r4d [initial_import]"
        exit(1)

    dataset = sys.argv[1]

    end_point = "http://192.168.0.190:3030/junk/data"

    import_data(dataset, end_point)
