linked-development-crawler
==========================

CABI - Linked Development API Crawler

To use this, you will need to run it in a Docker.

1. Initial Import
=================

You must create an initial import of the data into your fuseki
instance to do this run the following commands:

    $ docker build -t crawler .

    $ docker run -t -i crawler /home/crawler/crawler/import-data.py eldis initial_import

    $ docker run -t -i crawler /home/crawler/crawler/import-data.py r4d initial_import

2. Recurring Imports
====================

Subsequent data imports (for example on a crontab) can be run like
this:

     $ docker run -t -i crawler /home/crawler/crawler/import-data.py eldis

     $ docker run -t -i crawler /home/crawler/crawler/import-data.py r4d


Development
===========

These scripts were provided by CABI and mofified to work with PMD.
They still contain a number of hard coded assumptions on their
environment (e.g. global system paths), which mean that they're best
always run in a contained docker environment.

If you're wanting to hack on this inside the docker environment use
the following command to (re)build, tag and execute the environment
with your changes:

    $ docker build -t crawler . && docker run -t -i crawler /home/crawler/crawler/import-data.py eldis
