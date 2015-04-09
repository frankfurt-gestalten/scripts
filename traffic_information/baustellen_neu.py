#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

import lxml.etree


def getFirstElement(etree, xmlTag):
    return [x.text for x in etree.iter(xmlTag)][0]


def getTrafficInformationFromEtree(etree):
    for situation in etree.iter('{http://datex2.eu/schema/2/2_0}situation'):
        try:
            baustelle = {
                "id": situation.get('id'),
                "start": getFirstElement(situation, '{http://datex2.eu/schema/2/2_0}overallStartTime'),
                "end": getFirstElement(situation, '{http://datex2.eu/schema/2/2_0}overallEndTime'),
                "latitude": getFirstElement(situation, '{http://datex2.eu/schema/2/2_0}latitude'),
                "longitude": getFirstElement(situation, '{http://datex2.eu/schema/2/2_0}longitude'),
            }
        except IndexError as error:
            print(" --> Failed to get first element! id: {0}. Error: {1}".format(situation.get('id'), error), file=sys.stderr)

        description = []
        # XML. All. The. Way. Down. Until. It. Hurts.
        # Whoever created this spec should quit his job now. FFS.
        for x in situation.iter('{http://datex2.eu/schema/2/2_0}generalPublicComment'):
            for comment in x.iter('{http://datex2.eu/schema/2/2_0}comment'):
                for values in comment.iter('{http://datex2.eu/schema/2/2_0}values'):
                    for value in comment.iter('{http://datex2.eu/schema/2/2_0}value'):
                        description.append(value.text)
            break

        description = ''.join(description).replace('|', ' ')
        if description:
            baustelle['description'] = description.strip()

        yield baustelle


if __name__ == '__main__':
    with open('ausgabedatei.xml') as eingabe:
        etree = lxml.etree.parse(eingabe)

    for traffic_info in getTrafficInformationFromEtree(etree):
        print(traffic_info)
    for traffic_info in getTrafficInformationFromEtree(etree):
        print("Info for {id} ({start} - {end}): {latitude} / {longitude}, description: {description}".format(**traffic_info))
