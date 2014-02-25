linked-development-crawler
==========================

CABI - Linked Development API Crawler

To use these scripts you will need the following pre-requisites:

- Python 2.7
- pip (The python package manager)
- pip install rdflib==3.1

The first time you run the script for a given dataset you should set
the initial_import flag.  e.g. for eldis data:

    import-data.py eldis initial_import

Once the import has finished you should find triples in your database.

Subsequent imports should use the following command:

    import-data.py eldis

This command imports triples to an existing dataset.


Docker
======

There is a docker setup included, however due to a
[suspected bug in docker](https://github.com/dotcloud/docker/issues/4329)
it is not currently fully working.

Instructions on running this with docker can be found below:

Docker Initial Import
---------------------

You must create an initial import of the data into your fuseki
instance to do this run the following commands:

    $ docker build -t crawler .

    $ docker run -t -i crawler /home/crawler/crawler/import-data.py eldis initial_import

    $ docker run -t -i crawler /home/crawler/crawler/import-data.py r4d initial_import

Docker Recurring Imports
------------------------

Subsequent data imports (for example on a crontab) can be run like
this:

     $ docker run -t -i crawler /home/crawler/crawler/import-data.py eldis

     $ docker run -t -i crawler /home/crawler/crawler/import-data.py r4d


Development
-----------

    $ docker build -t crawler . && docker run -t -i crawler /home/crawler/crawler/import-data.py eldis
