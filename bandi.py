#!/usr/bin/python3
import requests as req
import os
import sys
import xml.etree.ElementTree as ET

xml_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
tempfile = "temp-currencies.xml"
datafile = "currencies.csv"

def get_xml_data(url):
    # get xml data file from url and return with its content
    resp = req.get(url)
    if resp.status_code != 200:
        print("HTTP request to download data failed!")
        sys.exit(1)
    if len(resp.content) > 2000:
        print("xml input file is larger then 2000 byte!")
        sys.exit(2)
    print("xml content length:", len(resp.content))
    return resp.content

def open_output_file(fname):
    # open output csv file
    outfile_is_existing = os.path.isfile(fname)
    fp = open(fname, "a")
    if not outfile_is_existing:
        # print csv header first if file is not existing
        fp.write("date;EUR-HUF;EUR-USD;EUR-CHF;EUR-JPY\n")
    return fp

def write_daydata(fp, d):
    # todo: check if data is 'fresh enough' to write and not already in
    line = ""
    for val in d.values():
        line += val + ';'

    line = line[:-1] + '\n'
    print("line:", line)
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
    ftemp = open(tempfile, 'wb')
    ftemp.write(content)
    ftemp.close()

    # open output file
    outf = open_output_file(datafile)

    # parse data xml
    tree = ET.parse(tempfile)
    root = tree.getroot()
    dayd = get_daydata(root)

    write_daydata(outf, dayd)
    outf.close()
    print(dayd)

    print("Hello!")

if __name__ == '__main__':
    main()

