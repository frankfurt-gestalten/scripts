#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import lxml.etree
from baustellen_neu import getTrafficInformationFromEtree

TEMPLATE = u"""<?xml version="1.0" encoding="ISO-8859-1"?>
<Diensteserver>
    <Zeitstempel>
        <Datum>{date}</Datum>
        <Uhrzeit>{time}</Uhrzeit>
    </Zeitstempel>
    {events}
</Diensteserver>"""

EVENT_TEMPLATE = u"""<Ereignis>
    <Source-Id>{id}</Source-Id>
    <Text>{description}</Text>
    <MeldungsTextKurz/>
    <MeldungsTextLang>{description}</MeldungsTextLang>
    <ZeitraumVon>{start}</ZeitraumVon>
    <ZeitraumBis>{end}</ZeitraumBis>
    <Verortung>
        <Verortungselement Index="0" Typ="Kante">
            <Koordinaten Index="0">
                <X-Koordinate>{latitude}</X-Koordinate>
                <Y-Koordinate>{longitude}</Y-Koordinate>
            </Koordinaten>
        </Verortungselement>
    </Verortung>
</Ereignis>"""


def main():
    with open('ausgabedatei.xml') as eingabe:
        etree = lxml.etree.parse(eingabe)

    events = []
    for traffic_info in getTrafficInformationFromEtree(etree):
        if not 'description' in traffic_info:
            continue

        events.append(EVENT_TEMPLATE.format(**traffic_info))

    now = datetime.datetime.now()

    return TEMPLATE.format(
        date=now.strftime('%d.%m.%Y'),
        time=now.strftime('%H:%M:%S'),
        events='\n'.join(events)
    )


if __name__ == '__main__':
    print(main())
