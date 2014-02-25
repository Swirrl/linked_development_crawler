#!/usr/bin/env python

import sys
import os

def execute(command):
    print command
    return os.system(command)

def restore_snapshot(graph_endpoint, snapshot_file):
    execute("curl -f -X POST -H \"Content-Type: application/turtle\" -d @" + snapshot_file + " " + graph_endpoint)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: restore-graph.py end-point-url turtle-backup-file"
        print
        print "Note that the end-point-url should include the graph."
        print
        print "e.g. restore-graph.py http://192.168.0.190:3030/junk/data?graph=http://linked-development.org/eldis/ ./tmp/eldis.ttl"
        print
        exit(1)

    end_point = sys.argv[1] # "http://192.168.0.190:3030/junk/data?graph=http://linked-development.org/eldis"
    turtle_file = sys.argv[2]

    restore_snapshot(end_point, turtle_file)
