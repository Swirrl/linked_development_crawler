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

Licence
-------

Copyright (c) 2014 CABI & DFID.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with this program.  If not, see
<http://www.gnu.org/licenses/>.

If you are not able to comply with the terms of the AGPL license, you
can request an exemption or a commercial license by contacting Swirrl:
http://swirrl.com.
