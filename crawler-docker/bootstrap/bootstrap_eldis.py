#!/usr/bin/env python

"""
Copyright 2013 Neontribe ltd <neil@neontribe.co.uk>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


get and install an initial set of eldis data
put in place auto updates for it

"""

import os


def main():
    os.system('/bin/mkdir -p /tmp/cabi-crawl-data/eldis/rdf')
    os.system('/bin/echo http://linked-development.org/eldis/ > /tmp/cabi-crawl-data/eldis/rdf/global.graph')
    os.system('/usr/bin/touch /tmp/cabi-crawl-data/eldis/active')

    #os.system('/usr/bin/python /tmp/cabi-crawl-data/crawler/crawler/eldis/eldis_update.py')
    #so now look at add file to cron tab

    #fh = open('/etc/cron.d/eldis', 'w')
    #fh.write('0 0 * * 0 root /bin/bash /root/.profile;/usr/bin/python /opt/tools/eldis/eldis_update.py\n')
    #fh.close()

if __name__ == "__main__":
    main()
