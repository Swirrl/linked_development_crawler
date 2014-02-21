#!/usr/bin/env bash

function fail_fast {
    echo "Failed to bootstrap" 1>&2;
    exit 1
}

trap 'fail_fast' ERR

python /home/crawler/bootstrap/bootstrap_eldis.py
python /home/crawler/bootstrap/bootstrap_r4d.py
