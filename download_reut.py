"""
download_reut.py

Infinite loop downloader for "https://www.reuters.com/" using the amazing newspaper library. Output files are time-stamped and contain
128 cases.

TO RUN PROGRAM:

python3 download_reut.py

PROGRAMMING NOTES: None beyond the fact that ten years ago this would be a week of work

SYSTEM REQUIREMENTS
This program has been successfully run under Mac OS 10.13.6; it is standard Python 3.7 so it should also run in Unix or Windows. 

PROVENANCE:
Programmer: Philip A. Schrodt
            Parus Analytics
            Charlottesville, VA, 22901 U.S.A.
            http://parusanalytics.com

Copyright (c) 2019	Philip A. Schrodt.	All rights reserved.

This code is covered under the MIT license: http://opensource.org/licenses/MIT

Report bugs to: schrodt735@gmail.com

REVISION HISTORY:
27-Dec-18:	Initial version

=========================================================================================================
"""
import newspaper
import datetime
import time

SLEEP_DELAY = 1800  # download every half hour
MAX_CASES = 128
URL = "https://www.reuters.com/"
MEMOIZE = False # DEBUG
MEMOIZE = True
PREFIX = "REUT_"

reut_filter = ["/br.reuters.com/", "/video", "/fr.reuters.com/", "/www.reuters.tv/", "/jp.reuters.com/", "/de.reuters.com/", 
    "/ar.reuters.com/","/reuters.zendesk.com/","/ru.reuters.com/","/widerimage.reuters.com/","/cn.reuters.com/","/ara.reuters.com/",
    "/it.reuters.com/","/commentary-", "/mx.reuters.com/", "/es.reuters.com/"]

nfile = 1
fout = open(PREFIX + time.strftime("%Y%m%d-%H%M%S") + ".txt", "w")
print("Output file:", PREFIX + time.strftime("%Y%m%d-%H%M%S") + ".txt")
ncase = 0
while True:
    print(time.strftime("%Y%m%d-%H%M%S") + ": getting", URL)
    a_paper = newspaper.build(URL, memoize_articles=MEMOIZE)
    print(" ==> Found", a_paper.size(),"articles")
    if a_paper.size() > 0:
        oldcase = ncase
        for article in a_paper.articles:
            if "-" not in article.url: # section rather than article
                continue
            skip_it = False
            for li in reut_filter:
                if li in article.url:
                    skip_it = True
                    break
            if skip_it:
                print("   Skipping", article.url)
            else: 
                print("Writing",article.url)
                try:
                    article.download()
                    article.parse()
                    fout.write("URL: " + article.url + "\n")
                    if article.publish_date is None:
                        d = datetime.datetime.now().date()
                    else:
                        d = article.publish_date
                    fout.write("DATE: " + str(d) + "\n")
                    fout.write("TITLE: " + article.title + "\n")
                    fout.write("TEXT:\n" + article.text + "\n------------------------\n")
                    ncase += 1
                    if ncase >= MAX_CASES:
                        fout.close()
                        fout = open(PREFIX + time.strftime("%Y%m%d-%H%M%S") + ".txt", "w")
                        print("Output file:", PREFIX + time.strftime("%Y%m%d-%H%M%S") + ".txt")
                        ncase = 0
                        nfile += 1
                except:
                    print("  ==> Download failed")
        print("Wrote", ncase - oldcase, "articles")
        print("Articles in file", nfile, ":", ncase,"\n")

    time.sleep(SLEEP_DELAY)
