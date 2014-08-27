#! /usr/bin/env python
# -*- coding: utf-8 -*-

import lxml.etree


def getFirstElement(xmlTag):
    return [x.text for x in etree.iter(xmlTag)][0]


def getTrafficInformationFromEtree(etree):
    for situation in etree.iter('{http://datex2.eu/schema/2/2_0}situation'):
        baustelle = {
            "start": getFirstElement('{http://datex2.eu/schema/2/2_0}overallStartTime'),
            "end": getFirstElement('{http://datex2.eu/schema/2/2_0}overallEndTime'),
            "latitude": getFirstElement('{http://datex2.eu/schema/2/2_0}latitude'),
            "longitude": getFirstElement('{http://datex2.eu/schema/2/2_0}longitude'),
        }

        description = []
        # XML. All. The. Way. Down. Until. It. Hurts.
        # Whoever created this spec should quit his job now. FFS.
        for x in etree.iter('{http://datex2.eu/schema/2/2_0}generalPublicComment'):
            for comment in x.iter('{http://datex2.eu/schema/2/2_0}comment'):
                for values in comment.iter('{http://datex2.eu/schema/2/2_0}values'):
                    for value in comment.iter('{http://datex2.eu/schema/2/2_0}value'):
                        description.append(value.text)

        description = ''.join(description).replace('|', ' ')
        if description:
            baustelle['description'] = description

        yield baustelle


if __name__ == '__main__':
    with open('ausgabedatei.xml') as eingabe:
        etree = lxml.etree.parse(eingabe)

    for traffic_info in getTrafficInformationFromEtree(etree):
        print(traffic_info)
