linked-development-crawler
==========================

CABI - Linked Development API Crawler

To use these scripts you will need the following pre-requisites:

- Python 2.7
- pip (The python package manager)
- pip install rdflib==3.1

The first time you run the script for a given dataset you should set
the initial_import flag.  It takes as its second argument a URL for
the end point.  This should not include the ?graph URI parameter as
the script itself will append that depending on the dataset.

The initial_import flag need only be passed if the specified graph
does not exist in your store.

e.g. for eldis data:

    $ ./import-data.py eldis http://localhost:3030/end-point/path/ initial_import

Once the import has finished you should find triples in your database.

Subsequent imports should use the following command:

    $ ./import-data.py eldis http://localhost:3030/end-point/path/

This command imports triples to an existing dataset.  During the
operation it also creates a temporary graph called
http://linked-development.org/graphs/management which caontains the
triples found in the 503.nt file.  This allows the front end to check
whether an import is in progress, and return a graceful 503 error
during the import.

If the script fails during its execution it will leave the `tmp/`
directory for inspection and debugging.  Ideally this should be
removed before the script is run again.

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
