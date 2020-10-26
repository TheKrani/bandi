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
currency_list = ["HUF", "USD", "CHF", "JPY"]

def get_xml_data(url):
    # get xml data file from url and return with its content
    resp = req.get(url)
    if resp.status_code != 200:
        print("HTTP request to download data failed!")
        sys.exit(1)
    if len(resp.content) > 2000:
        print("xml input file is larger than 2000 byte!")
        sys.exit(2)
    return resp.content.decode('utf-8')

def open_output_file(fname, clist):
    # open output csv file
    outfile_is_existing = os.path.isfile(fname)
    fp = open(fname, "a+")
    if not outfile_is_existing:
        # create csv header first if the file did not exist before
        header = "date;"
        for item in clist:
            header += "EUR-" + item + ';'
        header = header[:-1] + '\n'
        fp.write(header)
    return fp

def get_last_line(fp):
    # return with the last line of the file pointed by fp
    fp.seek(0,0)
    for last_line in fp:
        pass
    return last_line

def write_daydata(fp, d, clist):
    up_to_date = False
    line = ""
    new_data_date = d['date']
    new_data_date = int(new_data_date.replace('-', ''))

    lastl = get_last_line(fp)
    last_date = re.match(r'^\d{4}-\d{2}-\d{2}', lastl)
    if last_date:
        last_date = last_date.group(0)
        last_date = int(last_date.replace('-', ''))

        # Check if available data is up to date
        if last_date >= new_data_date:
            up_to_date = True

    line = d['date'] + ';'
    for cname in clist:
        line += d[cname] + ';'

    line = line[:-1] + '\n'
    if not up_to_date:
        # write it only if the data is not up to date
        fp.write(line)
    else:
        print("Data is up-to date, no data written!")
    return

def get_daydata(root, clist):
    money = root[2][0]
    timedate = root[2][0].attrib['time']

    l = []
    for child in money:
        l.append(child.attrib)

    daydata = {'date': ''}
    daydata['date'] = timedate
    for item in l:
        if item['currency'] in clist:
            daydata[item['currency']] = item['rate']
        else:
            pass
    return daydata

def main():
    # get xml data and write it to file
    content = get_xml_data(xml_url)

    # open output file
    outf = open_output_file(datafile, currency_list)

    # parse data xml
    root = ET.fromstring(content)
    dayd = get_daydata(root, currency_list)

    write_daydata(outf, dayd, currency_list)
    outf.close()

if __name__ == '__main__':
    main()

