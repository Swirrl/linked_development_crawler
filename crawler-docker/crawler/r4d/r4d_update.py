#!/usr/bin/env python

"""
copyright neontribe ltd 2013 neil@neontribe.co.uk

updates r4d data weekly

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


empties /home/r4d/rdf
get new files
makes new global.graph

imports into choosen database

this is the old plan, currently everytime i try to rename a graph, virtuoso segfaults
issues isql commands to remove eldis graph, then renames new one

this is the new plan
clear rdf data
download new datestamped files
delete graph
import new graph.
"""

import os
import datetime


def main():
    os.system('/bin/rm -rf /tmp/cabi-crawl-data/r4d/rdf/*')
    os.system('/bin/mkdir -p /tmp/cabi-crawl-data/r4d/rdf/new')
    os.system('/bin/echo http://linked-development.org/r4d/ > /tmp/cabi-crawl-data/r4d/rdf/global.graph')

    os.system('/usr/bin/wget  http://www.dfid.gov.uk/r4d/rdf/R4DOutputsData.zip')
    os.system('/bin/mv R4DOutputsData.zip /tmp/cabi-crawl-data/r4d/rdf/new/R4DOutputsData.zip')
    #unpack r4d data
    os.system('/usr/bin/unzip /tmp/cabi-crawl-data/r4d/rdf/new/R4DOutputsData.zip -d /tmp/cabi-crawl-data/r4d/rdf/new')
    os.system('/bin/rm -f /tmp/cabi-crawl-data/r4d/rdf/new/R4DOutputsData.zip')

    #Get the FAO Ontology as well
    os.system('/usr/bin/wget  http://www.fao.org/countryprofiles/geoinfo/geopolitical/data')
    os.system('/bin/mv data /tmp/cabi-crawl-data/r4d/rdf/new/fao.rdf')

    # And get Agrovoc
    os.system('/usr/bin/wget ftp://ftp.fao.org/gi/gil/gilws/aims/kos/agrovoc_formats/current/agrovoc.skos.xml.en.zip')
    os.system('/bin/mv agrovoc.skos.xml.en.zip /tmp/cabi-crawl-data/r4d/rdf/new/agrovoc.skos.xml.en.zip')
    #unpack r4d data
    os.system('/usr/bin/unzip /tmp/cabi-crawl-data/r4d/rdf/new/agrovoc.skos.xml.en.zip -d /tmp/cabi-crawl-data/r4d/rdf/new')
    os.system('/bin/rm -f /tmp/cabi-crawl-data/r4d/rdf/new/agrovoc.skos.xml.en.zip')

    #now copy to rdf folder with todays datestamp. The reason being
    #that we clear the graph before importing new data, if the new
    #data files names have not changed they are not by default imported
    #leaving an empty graph.
    date = datetime.date.today().isoformat()
    os.system('cd /tmp/cabi-crawl-data/r4d/rdf/new/; for f in *.rdf; do /bin/mv /tmp/cabi-crawl-data/r4d/rdf/new/"$f" /tmp/cabi-crawl-data/r4d/rdf/' +
                 date + '"$f"; done')
    os.system('/bin/rmdir /tmp/cabi-crawl-data/r4d/rdf/new')

    #Run SED to switch the URL base
    print "Running SED replacements"
    os.system('cd /tmp/cabi-crawl-data/r4d/rdf/; /bin/sed -i "s/r4d.dfid.gov.uk\/Output/linked-development.org\/r4d\/output/g" *.rdf')
    os.system('cd /tmp/cabi-crawl-data/r4d/rdf/; /bin/sed -i "s/r4d.dfid.gov.uk\/Project/linked-development.org\/r4d\/project/g" *.rdf')
    os.system('cd /tmp/cabi-crawl-data/r4d/rdf/; /bin/sed -i "s/r4d.dfid.gov.uk\/Organisation/linked-development.org\/r4d\/organisation/g" *.rdf')



if __name__ == "__main__":
    main()
