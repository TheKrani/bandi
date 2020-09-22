#!/usr/bin/python3
import requests as req
import os
import sys
import xml.etree.ElementTree as ET
import re
import datetime

# configuration
xml_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
datafile = "currencies.csv"

def get_xml_data(url):
    # get xml data file from url and return with its content
    resp = req.get(url)
    if resp.status_code != 200:
        print("HTTP request to download data failed!")
        sys.exit(1)
    if len(resp.content) > 2000:
        print("xml input file is larger than 2000 byte!")
        sys.exit(2)
    print("xml content length:", len(resp.content))
    return resp.content.decode('utf-8')

def open_output_file(fname):
    # open output csv file
    outfile_is_existing = os.path.isfile(fname)
    fp = open(fname, "a+")
    if not outfile_is_existing:
        # print csv header first if file is not existing
        fp.write("date;EUR-HUF;EUR-USD;EUR-CHF;EUR-JPY\n")
    return fp

def get_last_line(fp):
    # return with the last line of the file pointed by fp
    fp.seek(0,0)
    for last_line in fp:
        pass
    print("last line: ", last_line)
    return last_line

def write_daydata(fp, d):
    # todo: check if data is 'fresh enough' to write and not already in
    up_to_date = False
    line = ""
    now = datetime.datetime.now()
    now = int(now.strftime("%Y%m%d"))
    print("@ now: ", now)
    lastl = get_last_line(fp)
    last_date = re.match(r'^\d{4}-\d{2}-\d{2}', lastl)
    if last_date:
        last_date = last_date.group(0)
        last_date = int(last_date.replace('-', ''))
        print("@ last_date: ", last_date)
        if last_date >= now:
            up_to_date = True

    for val in d.values():
        line += val + ';'

    line = line[:-1] + '\n'
    print("@ line to be written:",line)
    if not up_to_date:
        # write it only if the data is not up to date
        fp.write(line)
    return

def get_daydata(root):
    money = root[2][0]
    timedate = root[2][0].attrib['time']
    print("timedate for the data: ", timedate)
    l = []
    for child in money:
        l.append(child.attrib)

    daydata = {'date': '', 'huf': 0, 'usd' : 0, 'chf' : 0, 'jpy' : 0}
    daydata['date'] = timedate
    for item in l:
        print(item)
        if item['currency'] == 'HUF':
            daydata['huf'] = item['rate']
        elif item['currency'] == 'USD':
            daydata['usd'] = item['rate']
        elif item['currency'] == 'CHF':
            daydata['chf'] = item['rate']
        elif item['currency'] == 'JPY':
            daydata['jpy'] = item['rate']
        else:
            pass
    return daydata

def main():
    # get xml data and write it to file
    content = get_xml_data(xml_url)

    # open output file
    outf = open_output_file(datafile)

    # parse data xml
    root = ET.fromstring(content)
    dayd = get_daydata(root)

    write_daydata(outf, dayd)
    outf.close()
    print(dayd)

    print("Hello!")

if __name__ == '__main__':
    main()

