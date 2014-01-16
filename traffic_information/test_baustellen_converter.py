#-*- coding: utf-8 -*-

import unittest
from baustellen_converter import convert_existing_coordinates


class XMLProcessingTest(unittest.TestCase):
    def test_complete_file_parsing(self):
        """
        Tests the parsing of a complete XML file.
        """
        filecontent = ['<?xml version="1.0" encoding="ISO-8859-1"?>\r\n',
        '<Diensteserver>\r\n',
        '    <Zeitstempel>\r\n',
        '        <Datum>08.06.2012</Datum>\r\n',
        '        <Uhrzeit>05:00:08</Uhrzeit>\r\n',
        '    </Zeitstempel>\r\n',
        '    <Ereignis>\r\n',
        '        <Source-Id>210465947490</Source-Id>\r\n',
        '        <Text>Sperrung Mainkai 9. - 10.6.</Text>\r\n',
        '        <MeldungsTextKurz/>\r\n',
        '        <MeldungsTextLang>Altstadt Mainkai, Untermainkai Vollsperrung zwischen Alte Br\xfccke und Untermainbr\xfccke wegen einer Veranstaltung. Am 9.6. von 09:00 Uhr morgens bis 01:00 Uhr nachts und am 10.6. von 11:30 Uhr bis 16 Uhr.</MeldungsTextLang>\r\n',
        '        <ZeitraumVon>05.06.2012 13:11:30</ZeitraumVon>\r\n',
        '        <ZeitraumBis>10.06.2012 16:00:00</ZeitraumBis>\r\n',
        '        <Phrasecode>C1</Phrasecode>\r\n',
        '        <AlertCNr>401</AlertCNr>\r\n',
        '        <Verortung>\r\n',
        '            <LCL-Verortung>\r\n',
        '                <Version>7.0</Version>\r\n',
        '                <Primary-Location>44430</Primary-Location>\r\n',
        '                <Secondary-Location>44431</Secondary-Location>\r\n',
        '            </LCL-Verortung>\r\n',
        '            <Verortungselement Index="0" Typ="Kante">\r\n',
        '                <Koordinaten Index="0">\r\n',
        '                    <X-Koordinate>3477557,06</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552626,62</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="1">\r\n',
        '                    <X-Koordinate>3477472,40</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552618,27</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="2">\r\n',
        '                    <X-Koordinate>3477459,30</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552616,00</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '            </Verortungselement>\r\n',
        '            <Verortungselement Index="3" Typ="Kante">\r\n',
        '                <Koordinaten Index="0">\r\n',
        '                    <X-Koordinate>3477459,30</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552616,00</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="1">\r\n',
        '                    <X-Koordinate>3477443,95</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552613,34</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="2">\r\n',
        '                    <X-Koordinate>3477427,27</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552610,44</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="3">\r\n',
        '                    <X-Koordinate>3477344,29</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552589,32</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '            </Verortungselement>\r\n',
        '            <Verortungselement Index="7" Typ="Kante">\r\n',
        '                <Koordinaten Index="0">\r\n',
        '                    <X-Koordinate>3477344,29</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552589,32</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="1">\r\n',
        '                    <X-Koordinate>3477326,29</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552584,47</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="2">\r\n',
        '                    <X-Koordinate>3477309,42</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552579,92</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '            </Verortungselement>\r\n',
        '            <Verortungselement Index="10" Typ="Kante">\r\n',
        '                <Koordinaten Index="0">\r\n',
        '                    <X-Koordinate>3477309,42</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552579,92</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="1">\r\n',
        '                    <X-Koordinate>3477302,52</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552578,06</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="2">\r\n',
        '                    <X-Koordinate>3477253,68</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552564,89</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="3">\r\n',
        '                    <X-Koordinate>3477235,58</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552558,69</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '            </Verortungselement>\r\n',
        '            <Verortungselement Index="14" Typ="Kante">\r\n',
        '                <Koordinaten Index="0">\r\n',
        '                    <X-Koordinate>3477235,58</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552558,69</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="1">\r\n',
        '                    <X-Koordinate>3477207,82</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552549,18</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="2">\r\n',
        '                    <X-Koordinate>3477185,97</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552540,20</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '            </Verortungselement>\r\n',
        '            <Verortungselement Index="17" Typ="Kante">\r\n',
        '                <Koordinaten Index="0">\r\n',
        '                    <X-Koordinate>3477185,97</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552540,20</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="1">\r\n',
        '                    <X-Koordinate>3477119,05</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552512,68</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '            </Verortungselement>\r\n',
        '            <Verortungselement Index="19" Typ="Kante">\r\n',
        '                <Koordinaten Index="0">\r\n',
        '                    <X-Koordinate>3477119,05</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552512,68</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="1">\r\n',
        '                    <X-Koordinate>3477040,42</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552481,76</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="2">\r\n',
        '                    <X-Koordinate>3476909,21</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552428,54</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '                <Koordinaten Index="3">\r\n',
        '                    <X-Koordinate>3476882,43</X-Koordinate>\r\n',
        '                    <Y-Koordinate>5552424,77</Y-Koordinate>\r\n',
        '                </Koordinaten>\r\n',
        '            </Verortungselement>\r\n',
        '        </Verortung>\r\n',
        '    </Ereignis>\r\n',
        '    <Ereignis>\r\n',
        '        <Source-Id>210425353395</Source-Id>\r\n',
        '        <Text>Parkhaus R\xf6mer geschlossen</Text>\r\n',
        '        <MeldungsTextKurz/>\r\n',
        '        <MeldungsTextLang>Altstadt Parkhaus R\xf6mer Aufgrund von Umbauarbeiten und Sanierungsarbeiten des Parkhauses und wegen Vorbereitungsarbeiten f\xfcr die Bebauung des Altstadtareals, bleibt das Parkhaus voraussichtlich bis November 2012 geschlossen.</MeldungsTextLang>\r\n',
        '        <ZeitraumVon>26.04.2011 14:49:55</ZeitraumVon>\r\n',
        '        <ZeitraumBis>15.11.2012 06:00:00</ZeitraumBis>\r\n',
        '        <Phrasecode>X45</Phrasecode>\r\n',
        '        <AlertCNr>1924</AlertCNr>\r\n',
        '        <Verortung/>\r\n',
        '    </Ereignis>\r\n',
        '</Diensteserver>\r\n']

        expected_result = ['<?xml version="1.0" encoding="ISO-8859-1"?>',
        '<Diensteserver>',
        '    <Zeitstempel>',
        '        <Datum>08.06.2012</Datum>',
        '        <Uhrzeit>05:00:08</Uhrzeit>',
        '    </Zeitstempel>',
        '    <Ereignis>',
        '        <Source-Id>210465947490</Source-Id>',
        '        <Text>Sperrung Mainkai 9. - 10.6.</Text>',
        '        <MeldungsTextKurz/>',
        '        <MeldungsTextLang>Altstadt Mainkai, Untermainkai Vollsperrung zwischen Alte Br\xfccke und Untermainbr\xfccke wegen einer Veranstaltung. Am 9.6. von 09:00 Uhr morgens bis 01:00 Uhr nachts und am 10.6. von 11:30 Uhr bis 16 Uhr.</MeldungsTextLang>',
        '        <ZeitraumVon>05.06.2012 13:11:30</ZeitraumVon>',
        '        <ZeitraumBis>10.06.2012 16:00:00</ZeitraumBis>',
        '        <Phrasecode>C1</Phrasecode>',
        '        <AlertCNr>401</AlertCNr>',
        '        <Verortung>',
        '            <LCL-Verortung>',
        '                <Version>7.0</Version>',
        '                <Primary-Location>44430</Primary-Location>',
        '                <Secondary-Location>44431</Secondary-Location>',
        '            </LCL-Verortung>',
        '            <Verortungselement Index="0" Typ="Kante">',
        '                <Koordinaten Index="0">',
        '                    <X-Koordinate>50.1094376568</X-Koordinate>',
        '                    <Y-Koordinate>8.68520351843</Y-Koordinate>',
        '                </Koordinaten>',
        '            </Verortungselement>',
        '        </Verortung>',
        '    </Ereignis>',
        '    <Ereignis>',
        '        <Source-Id>210425353395</Source-Id>',
        '        <Text>Parkhaus R\xf6mer geschlossen</Text>',
        '        <MeldungsTextKurz/>',
        '        <MeldungsTextLang>Altstadt Parkhaus R\xf6mer Aufgrund von Umbauarbeiten und Sanierungsarbeiten des Parkhauses und wegen Vorbereitungsarbeiten f\xfcr die Bebauung des Altstadtareals, bleibt das Parkhaus voraussichtlich bis November 2012 geschlossen.</MeldungsTextLang>',
        '        <ZeitraumVon>26.04.2011 14:49:55</ZeitraumVon>',
        '        <ZeitraumBis>15.11.2012 06:00:00</ZeitraumBis>',
        '        <Phrasecode>X45</Phrasecode>',
        '        <AlertCNr>1924</AlertCNr>',
        '        <Verortung/>',
        '    </Ereignis>',
        '</Diensteserver>']

        self.assertEqual(expected_result, convert_existing_coordinates(filecontent))

    def test_finding_elements(self):
        """
        Tests the right finding of an element.
        """
        filecontent = ['            <Verortungselement Index="0" Typ="Kante">\r\n',
            '                <Koordinaten Index="0">\r\n',
            '                    <X-Koordinate>3477557,06</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552626,62</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="1">\r\n',
            '                    <X-Koordinate>3477472,40</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552618,27</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="2">\r\n',
            '                    <X-Koordinate>3477459,30</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552616,00</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '            </Verortungselement>\r\n',
            '            <Verortungselement Index="3" Typ="Kante">\r\n',
            '                <Koordinaten Index="0">\r\n',
            '                    <X-Koordinate>3477459,30</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552616,00</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="1">\r\n',
            '                    <X-Koordinate>3477443,95</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552613,34</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="2">\r\n',
            '                    <X-Koordinate>3477427,27</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552610,44</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="3">\r\n',
            '                    <X-Koordinate>3477344,29</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552589,32</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '            </Verortungselement>\r\n',
            '            <Verortungselement Index="7" Typ="Kante">\r\n',
            '                <Koordinaten Index="0">\r\n',
            '                    <X-Koordinate>3477344,29</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552589,32</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="1">\r\n',
            '                    <X-Koordinate>3477326,29</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552584,47</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="2">\r\n',
            '                    <X-Koordinate>3477309,42</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552579,92</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '            </Verortungselement>\r\n',
            '            <Verortungselement Index="10" Typ="Kante">\r\n',
            '                <Koordinaten Index="0">\r\n',
            '                    <X-Koordinate>3477309,42</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552579,92</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="1">\r\n',
            '                    <X-Koordinate>3477302,52</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552578,06</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="2">\r\n',
            '                    <X-Koordinate>3477253,68</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552564,89</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="3">\r\n',
            '                    <X-Koordinate>3477235,58</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552558,69</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '            </Verortungselement>\r\n',
            '            <Verortungselement Index="14" Typ="Kante">\r\n',
            '                <Koordinaten Index="0">\r\n',
            '                    <X-Koordinate>3477235,58</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552558,69</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="1">\r\n',
            '                    <X-Koordinate>3477207,82</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552549,18</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="2">\r\n',
            '                    <X-Koordinate>3477185,97</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552540,20</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '            </Verortungselement>\r\n',
            '            <Verortungselement Index="17" Typ="Kante">\r\n',
            '                <Koordinaten Index="0">\r\n',
            '                    <X-Koordinate>3477185,97</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552540,20</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="1">\r\n',
            '                    <X-Koordinate>3477119,05</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552512,68</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '            </Verortungselement>\r\n',
            '            <Verortungselement Index="19" Typ="Kante">\r\n',
            '                <Koordinaten Index="0">\r\n',
            '                    <X-Koordinate>3477119,05</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552512,68</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="1">\r\n',
            '                    <X-Koordinate>3477040,42</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552481,76</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="2">\r\n',
            '                    <X-Koordinate>3476909,21</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552428,54</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '                <Koordinaten Index="3">\r\n',
            '                    <X-Koordinate>3476882,43</X-Koordinate>\r\n',
            '                    <Y-Koordinate>5552424,77</Y-Koordinate>\r\n',
            '                </Koordinaten>\r\n',
            '            </Verortungselement>\r\n',
            '        </Verortung>\r\n']

        expected_result = ['            <Verortungselement Index="0" Typ="Kante">',
            '                <Koordinaten Index="0">',
            '                    <X-Koordinate>50.1094376568</X-Koordinate>',
            '                    <Y-Koordinate>8.68520351843</Y-Koordinate>',
            '                </Koordinaten>',
            '            </Verortungselement>',
            '        </Verortung>']

        self.assertEqual(expected_result, convert_existing_coordinates(filecontent))


    def test_simple_input(self):
        """
        Tests a very simple and limited input.
        """
        filecontent = ['            <Verortungselement Index="0" Typ="Kante">\r\n',
                   '                <Koordinaten Index="0">\r\n',
                   '                    <X-Koordinate>3477119,05</X-Koordinate>\r\n',
                   '                    <Y-Koordinate>5552512,68</Y-Koordinate>\r\n',
                   '                </Koordinaten>\r\n',
                   '                <Koordinaten Index="1">\r\n',
                   '                    <X-Koordinate>3477040,42</X-Koordinate>\r\n',
                   '                    <Y-Koordinate>5552481,76</Y-Koordinate>\r\n',
                   '                </Koordinaten>\r\n',
                   '                <Koordinaten Index="2">\r\n',
                   '                    <X-Koordinate>3476909,21</X-Koordinate>\r\n',
                   '                    <Y-Koordinate>5552428,54</Y-Koordinate>\r\n',
                   '                </Koordinaten>\r\n',
                   '                <Koordinaten Index="3">\r\n',
                   '                    <X-Koordinate>3476882,43</X-Koordinate>\r\n',
                   '                    <Y-Koordinate>5552424,77</Y-Koordinate>\r\n',
                   '                </Koordinaten>\r\n',
                   '            </Verortungselement>\r\n']

        expected_result = ['            <Verortungselement Index="0" Typ="Kante">',
                   '                <Koordinaten Index="0">',
                   '                    <X-Koordinate>50.1083965577</X-Koordinate>',
                   '                    <Y-Koordinate>8.67908724506</Y-Koordinate>',
                   '                </Koordinaten>',
                   '            </Verortungselement>']
        self.assertEqual(expected_result, convert_existing_coordinates(filecontent))

    def testOutputDoesNotContainMultipleKoordinatesForOneVerortungselement(self):
        filecontent = ['<?xml version="1.0" encoding="ISO-8859-1"?>',
        '<Diensteserver>',
        '    <Zeitstempel>',
        '        <Datum>07.01.2014</Datum>',
        '        <Uhrzeit>08:05:17</Uhrzeit>',
        '    </Zeitstempel>',
        '    <Ereignis>',
        '        <Source-Id>210523955526</Source-Id>',
        '        <Text>Verkehrsführung Rebstockgelände 8. bis 11.1.</Text>',
        '        <MeldungsTextKurz/>',
        '        <MeldungsTextLang>Bla</MeldungsTextLang>',
        '        <ZeitraumVon>06.01.2014 15:25:26</ZeitraumVon>',
        '        <ZeitraumBis>11.01.2014 20:00:00</ZeitraumBis>',
        '        <Phrasecode/>',
        '        <AlertCNr>1854</AlertCNr>',
        '        <Verortung>',
        '            <Verortungselement Index="0" Typ="Kante">',
        '                <Koordinaten Index="0">',
        '                    <X-Koordinate>3471498,10</X-Koordinate>',
        '                    <Y-Koordinate>5552883,99</Y-Koordinate>',
        '                </Koordinaten>',
        '            </Verortungselement>',
        '        </Verortung>',
        '    </Ereignis>',
        '    <Ereignis>',
        '        <Source-Id>210523955335</Source-Id>',
        '        <Text>Heimtextil 8. bis 11.1.</Text>',
        '        <MeldungsTextKurz/>',
        '        <MeldungsTextLang>Blabla</MeldungsTextLang>',
        '        <ZeitraumVon>06.01.2014 15:22:15</ZeitraumVon>',
        '        <ZeitraumBis>11.01.2014 20:00:00</ZeitraumBis>',
        '        <Phrasecode/>',
        '        <AlertCNr>1469</AlertCNr>',
        '        <Verortung>',
        '            <LCL-Verortung>',
        '                <Version>7.0</Version>',
        '                <Primary-Location>23580</Primary-Location>',
        '                <Secondary-Location>23581</Secondary-Location>',
        '            </LCL-Verortung>',
        '            <Verortungselement Index="0" Typ="Kante">',
        '                <Koordinaten Index="0">',
        '                    <X-Koordinate>3474728,38</X-Koordinate>',
        '                    <Y-Koordinate>5553121,92</Y-Koordinate>',
        '                </Koordinaten>',
        '            </Verortungselement>',
        '        </Verortung>',
        '    </Ereignis>',
        '</Diensteserver>',]

        expected_result = [
            '<?xml version="1.0" encoding="ISO-8859-1"?>',
            '<Diensteserver>',
            '    <Zeitstempel>',
            '        <Datum>07.01.2014</Datum>',
            '        <Uhrzeit>08:05:17</Uhrzeit>',
            '    </Zeitstempel>',
            '    <Ereignis>',
            '        <Source-Id>210523955526</Source-Id>',
            '        <Text>Verkehrsf\xc3\xbchrung Rebstockgel\xc3\xa4nde 8. bis 11.1.</Text>',
            '        <MeldungsTextKurz/>',
            '        <MeldungsTextLang>Bla</MeldungsTextLang>',
            '        <ZeitraumVon>06.01.2014 15:25:26</ZeitraumVon>',
            '        <ZeitraumBis>11.01.2014 20:00:00</ZeitraumBis>',
            '        <Phrasecode/>',
            '        <AlertCNr>1854</AlertCNr>',
            '        <Verortung>',
            '            <Verortungselement Index="0" Typ="Kante">',
            '                <Koordinaten Index="0">',
            '                    <X-Koordinate>50.1114909639</X-Koordinate>',
            '                    <Y-Koordinate>8.60048420076</Y-Koordinate>',
            '                </Koordinaten>',
            '            </Verortungselement>',
            '        </Verortung>',
            '    </Ereignis>',
            '    <Ereignis>',
            '        <Source-Id>210523955335</Source-Id>',
            '        <Text>Heimtextil 8. bis 11.1.</Text>',
            '        <MeldungsTextKurz/>',
            '        <MeldungsTextLang>Blabla</MeldungsTextLang>',
            '        <ZeitraumVon>06.01.2014 15:22:15</ZeitraumVon>',
            '        <ZeitraumBis>11.01.2014 20:00:00</ZeitraumBis>',
            '        <Phrasecode/>',
            '        <AlertCNr>1469</AlertCNr>',
            '        <Verortung>',
            '            <LCL-Verortung>',
            '                <Version>7.0</Version>',
            '                <Primary-Location>23580</Primary-Location>',
            '                <Secondary-Location>23581</Secondary-Location>',
            '            </LCL-Verortung>',
            '            <Verortungselement Index="0" Typ="Kante">',
            '                <Koordinaten Index="0">',
            '                    <X-Koordinate>50.1137765589</X-Koordinate>',
            '                    <Y-Koordinate>8.64562752036</Y-Koordinate>',
            '                </Koordinaten>',
            '            </Verortungselement>',
            '        </Verortung>',
            '    </Ereignis>',
            '</Diensteserver>'
        ]

        self.maxDiff = None
        self.assertEqual(expected_result, convert_existing_coordinates(filecontent))


if __name__ == '__main__':
    unittest.main()
