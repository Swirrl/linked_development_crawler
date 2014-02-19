#!/usr/bin/env bash

function fail_fast {
    echo "Failed to bootstrap" 1>&2;
    exit 1
}

trap 'fail_fast' ERR 

sudo apt-get -y install zip

python /vagrant//bootstrap/bootstrap_eldis.py
python /vagrant/bootstrap/bootstrap_r4d.py
