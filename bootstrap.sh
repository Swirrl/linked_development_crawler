#!/usr/bin/env bash

function fail_fast {
    echo "Failed to bootstrap"
    exit 1
}

trap 'fail_fast' ERR 

./bootstrap/bootstrap_eldis.py
./bootstrap/bootstrap_r4d.py
