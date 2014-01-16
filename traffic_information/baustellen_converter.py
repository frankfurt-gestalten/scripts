#! python
#-*- coding: utf-8 -*-
import logging
import os
import re
import sys
import tempfile
from optparse import OptionParser
from collections import namedtuple

from GKConverter import gkconverter

logger = logging.getLogger('BAUSTELLEN_LOGGER')


def convert_existing_coordinates(xml_content):
    def remove_newlines(line):
        line = line.replace('\n', '')
        return line.replace('\r', '')

    def not_in_an_verortungselement():
        return not elem and not elemKO

    stuff_to_return = []
    CoordinatesLine = namedtuple('CoordinatesLine', ['pre', 'value', 'post'])

    #Preparing regexp
    verortungselement_start = re.compile("\<Verortungselement Index=\"(\d+)\".*\>", re.I)
    verortungselement_ende = re.compile("\<\/Verortungselement\>", re.I)
    verortungs_start = re.compile("\<Verortung.*\>", re.I)
    koord_element = re.compile("\<Koordinaten Index=\"(\d+)\".*\>", re.I)
    koord_element_start = re.compile("\<Koordinaten.*\>", re.I)
    koordinaten_ende = re.compile("\<\/Koordinaten\>", re.I)
    x_koord = re.compile("(.*<X-Koordinate>)([0-9]+,[0-9]+)(<\/X-Koordinate>.*)", re.I)
    y_koord = re.compile("(.*<Y-Koordinate>)([0-9]+,[0-9]+)(<\/Y-Koordinate>.*)", re.I)

    #Variables used during the run
    x = None
    y = None
    elem = 0
    elemKO = 0
    found_x_coordinate = None
    found_y_coordinate = None
    koords_used = False

    for line in xml_content:
        line = remove_newlines(line)

        if koords_used:
            stuff_to_return.append(line)
            koords_used = False
            continue

        verort = verortungselement_start.search(line)
        koo = koord_element.search(line)
        if(verort):
            elem = int(verort.group(1))
        elif(verortungs_start.search(line)):
            elem = 0
        elif(koo):
            elemKO = int(koo.group(1))
        elif(koord_element_start.search(line)):
            elemKO = 0

        if not found_x_coordinate:
            found_x_coordinate = x_koord.search(line)
        if not found_y_coordinate:
            found_y_coordinate = y_koord.search(line)

        if(elemKO == 0 and found_x_coordinate and not found_y_coordinate):
            x = CoordinatesLine(found_x_coordinate.group(1), found_x_coordinate.group(2), found_x_coordinate.group(3))
        elif(elemKO == 0 and found_y_coordinate):
            y = CoordinatesLine(found_y_coordinate.group(1), found_y_coordinate.group(2), found_y_coordinate.group(3))
        elif not_in_an_verortungselement():
            stuff_to_return.append(line)

        if(x and y and elemKO == 0 and elem == 0 and not koords_used):
            float_x = float(x.value.replace(',', '.'))
            float_y = float(y.value.replace(',', '.'))
            (converted_x, converted_y) = gkconverter.convert_GK_to_lat_long(float_x, float_y)

            logger.debug(
                '\n\nPosting coordinates: {0}'.format(
                    [
                        '{0} -> {1}'.format(key, locals()[key]) for key in
                        (
                            'verort', 'koords_used', 'elem', 'elemKO', 'found_x_coordinate',
                            'found_y_coordinate', 'y', 'x', 'line'
                        )
                    ]
                )
            )

            stuff_to_return.append("%s%s%s" % (x.pre, converted_x, x.post))
            stuff_to_return.append("%s%s%s" % (y.pre, converted_y, y.post))

            x = found_x_coordinate = None
            y = found_y_coordinate = None
            koords_used = True

        #Is any element ending, so we can start to print again?
        if(verortungselement_ende.search(line)):
            elem = None
            koords_used = False
        elif(koordinaten_ende.search(line)):
            elemKO = None
            x = found_x_coordinate = None
            y = found_y_coordinate = None

    return stuff_to_return


def get_options(args=None):
    parser = OptionParser()
    parser.add_option("-s", "--server", help="Server to fetch the import file from.")
    parser.add_option("-u", "--user", help="The user used to identify at the server.")
    parser.add_option("-p", "--password", help="The password for the user.")
    parser.add_option("-f", "--filename", help="Name of the file to fetch.")
    parser.add_option("-o", "--outputfile", help="Name of the file that will contain the converted output.")
    parser.add_option("-t", "--tempfile", help="Name of the temporary file used when fetching data. Will be removed after script execution.")
    parser.add_option("--debug", action="store_true", default=False,
                      help="Enables debug output.")

    (options, args) = parser.parse_args(args)

    config = {
        'server': options.server,
        'user': options.user,
        'password': options.password,
        'filename': options.filename,
        'outputfile': options.outputfile,
        'debug': options.debug,
    }

    if options.tempfile:
        config['tmp_file'] = options.tempfile

    return config


def run_standalone(config):
    logger.info('Started')
    if not 'tmp_file' in config:
        logger.debug('Getting tmp filename...')
        config['tmp_file'] = tempfile.mkstemp()[1]

    logger.debug('Will save temporary data into %(tmp_file)s' % config)

    logger.debug('Downloading %(filename)s from %(server)s to %(tmp_file)s' % config)
    download_command = 'wget --user=%(user)s --password=%(password)s %(server)s/%(filename)s -O %(tmp_file)s' % config
    logger.debug("Will use the following to download the file: %s" % download_command)
    os.system(download_command)

    if os.path.isfile(config['tmp_file']):
        logger.debug('File %(tmp_file)s exists, proceeding.' % config)

        with open(config['tmp_file'], 'r') as tmp_file, open(config['outputfile'], 'w') as out_file:
            new_content = convert_existing_coordinates(tmp_file)
            for line in new_content:
                out_file.write('%s\n' % line)

        os.remove(config['tmp_file'])
        logger.debug('Removed %(tmp_file)s' % config)
    else:
        logger.warning('The file %(tmp_file)s does not exist.' % config)

    logger.info('Finished')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        from config import configs
    except ImportError:
        config = get_options()
        configs = [config]

    for config in configs:
        if config['debug']:
            logger.setLevel(logging.DEBUG)

        run_standalone(config)
