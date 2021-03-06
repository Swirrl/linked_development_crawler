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

retry_delays = [0,1,1,2,3,5,8,13,21,34]

management_graph = "http://linked-development.org/graphs/management"

class UploadFailure(StandardError):
    pass

def execute(command, raise_on_error=True):
    print command
    ret = os.system(command)
    if raise_on_error and (not ret == 0):
        raise StandardError, "Aborting command failed ("+ str(ret) + "): " + command

    return ret

def post_data(update_endpoint, rdf_file, delays):
    delays = copy.copy(delays)
    time.sleep(delays.pop(0))
    command = "curl -f -X POST -H \"Content-Type: application/rdf+xml\" -d @" + rdf_file + " " + update_endpoint
    posted = execute(command, raise_on_error=False)

    while posted != 0:
        if not delays:
            raise UploadFailure('Failed to upload file after %s retries of command: %s ' %(len(retry_delays), command))
        time.sleep(delays.pop(0))
        print "retrying: " + command
        ret = os.system(command)

def is_initial_import():
    return len(sys.argv) == 4 and sys.argv[3] == "initial_import"

def fetch_snapshot(update_endpoint, snapshot_name):
    if not is_initial_import():
        snapshot_file = "./tmp/cabi-crawl-data/" + snapshot_name + "-snapshot.ttl"
        execute("curl -f -X GET -H \"Accept: application/turtle\" " + update_endpoint + " > " + snapshot_file)
    else:
        print "Initial import, not creating a snapshot"

def restore_snapshot(graph_endpoint, snapshot_name):
    if not is_initial_import():
        snapshot_file = "./tmp/cabi-crawl-data/" + snapshot_name + "-snapshot.ttl"
        ret = execute("curl -f -X POST -H \"Content-Type: application/turtle\" -d @" + snapshot_file + " " + graph_endpoint)
        if ret == 0:
            execute("rm " + snapshot_file)
    else:
        print "This is the initial run so there is nothing to restore."

def start_transaction():
    execute("touch /tmp/cabi-crawl-in-progress")

def end_transaction():
    execute("rm /tmp/cabi-crawl-in-progress")

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
        command = "./eldis/eldis_update.py"
    else:
        command = "./r4d/r4d_update.py"

    print "Fetching remote " + dataset_name + " data: " + command
    os.system(command) # delegate to update script

def import_data(dataset_name, endpoint):
    graph_uri = "http://linked-development.org/graph/" + dataset_name
    graph_endpoint = endpoint + "?graph=" + graph_uri
    base_path = "./tmp/cabi-crawl-data/" + dataset_name + "/rdf/"

    get_remote_data(dataset_name)

    fetch_snapshot(graph_endpoint, dataset_name)

    start_transaction()
    delete_graph(graph_endpoint)
    try:
        import_rdf_files(base_path, graph_endpoint)
    except Exception, e:
        print "Failed to import data attempting to restore last working set..."
        print e
        print traceback.print_exc()
        restore_snapshot(graph_endpoint, dataset_name)

    end_transaction()

def initialise():
    if not os.path.exists("./tmp"):
        execute('/bin/mkdir -p ./tmp/cabi-crawl-data/eldis/rdf')
        execute('/bin/echo http://linked-development.org/eldis/ > ./tmp/cabi-crawl-data/eldis/rdf/global.graph')
        execute('/usr/bin/touch ./tmp/cabi-crawl-data/eldis/active')

        execute('/bin/mkdir -p ./tmp/cabi-crawl-data/r4d/rdf')
        execute('/bin/echo http://linked-development.org/r4d/ > ./tmp/cabi-crawl-data/r4d/rdf/global.graph')
        execute('/usr/bin/touch ./tmp/cabi-crawl-data/r4d/active')

if __name__ == "__main__":

    # Change working directory to that of this script so we can use
    # relative paths from now on.
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    if not (len(sys.argv) == 3 or len(sys.argv) == 4):
        print "Usage: import-data.py eldis|r4d end-point [initial_import]"
        exit(1)

    dataset = sys.argv[1]

    end_point = sys.argv[2] # "http://192.168.0.190:3030/junk/data"

    initialise()

    import_data(dataset, end_point)
    execute("rm -rf ./tmp") # After a successful import remove all the data
