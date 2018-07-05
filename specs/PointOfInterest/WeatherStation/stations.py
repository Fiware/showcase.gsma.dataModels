#!bin/python
# -*- coding: utf-8 -*-

import csv


def main():
    csvoutput = open('stations-normalized.csv', 'wb')
    station_writer = csv.writer(csvoutput, delimiter=',')

    with open('stations.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        index = 0
        for row in reader:
            if index != 0:
                latitude = row[5].strip()
                longitude = row[6].strip()

                out_latitude = ''
                out_longitude = ''

                out_latitude = latitude[0:2]
                out_latitude += ' '
                out_latitude += latitude[2:4]
                out_latitude += ' '
                out_latitude += latitude[4:6]

                if longitude[6] == 'W':
                    out_longitude = '-'

                out_longitude += longitude[0:2]
                out_longitude += ' '
                out_longitude += longitude[2:4]
                out_longitude += ' '
                out_longitude += longitude[4:6]

                row[5] = out_latitude
                row[6] = out_longitude

            station_writer.writerow(row)
            index += 1


if __name__ == '__main__':
    main()
