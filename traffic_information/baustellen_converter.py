#! python
#-*- coding: utf-8 -*-
import logging
import os
import re
import sys
import tempfile
from optparse import OptionParser

from GKConverter import gkconverter

logger = logging.getLogger('BAUSTELLEN_LOGGER')


def convert_existing_coordinates(xml_content):
    stuff_to_return = []

    #Preparing regexp
    verortungselement_start = re.compile("\<Verortungselement Index=\"(\d+)\".*\>", re.I)
    verortungselement_ende = re.compile("\<\/Verortungselement\>", re.I)
    verortungselement = re.compile("\<Verortungselement.*\>", re.I)
    koord_element = re.compile("\<Koordinaten Index=\"(\d+)\".*\>", re.I)
    koord_element_start = re.compile("\<Koordinaten.*\>", re.I)
    koordinaten_ende = re.compile("\<\/Koordinaten\>", re.I)
    x_koord = re.compile("(.*<X-Koordinate>)([0-9]+,[0-9]+)(<\/X-Koordinate>.*)", re.I)
    y_koord = re.compile("(.*<Y-Koordinate>)([0-9]+,[0-9]+)(<\/Y-Koordinate>.*)", re.I)

    #Variables used during the run
    pre_X = x = post_X = None
    pre_Y = y = post_Y = None
    elem = 0
    elemKO = 0
    x_koo = None
    y_koo = None
    koords_used = False

    for line in xml_content:
        line = line.replace('\n', '')
        line = line.replace('\r', '')

        if koords_used:
            stuff_to_return.append(line)
            koords_used = False
            continue

        verort = verortungselement_start.search(line)
        koo = koord_element.search(line)
        if(verort):
            elem = int(verort.group(1))
        elif(verortungselement.search(line)):
            elem = 0
        elif(koo):
            elemKO = int(koo.group(1))
        elif(koord_element_start.search(line)):
            elemKO = 0

        if not x_koo:
            x_koo = x_koord.search(line)
        if not y_koo:
            y_koo = y_koord.search(line)

        if(elemKO == 0 and x_koo and not y_koo):
            pre_X = x_koo.group(1)
            x = x_koo.group(2)
            post_X = x_koo.group(3)
        elif(elemKO == 0 and y_koo):
            pre_Y = y_koo.group(1)
            y = y_koo.group(2)
            post_Y = y_koo.group(3)
        elif(not elem and not elemKO):
            stuff_to_return.append(line)

        if(x and y and elemKO == 0 and elem == 0 and not koords_used):
            float_x = float(x.replace(',', '.'))
            float_y = float(y.replace(',', '.'))
            (x, y) = gkconverter.convert_GK_to_lat_long(float_x, float_y)

            logger.debug(
                '\n\nPosting coordinates: {0}'.format(
                    ['{0} -> {1}'.format(key, locals()[key]) for key in
                        (
                            'verort', 'koords_used', 'elemKO', 'x_koo', 'elem',
                            'y_koo', 'y', 'x', 'line'
                        )
                    ]
                )
            )

            stuff_to_return.append("%s%s%s" % (pre_X, x, post_X))
            stuff_to_return.append("%s%s%s" % (pre_Y, y, post_Y))

            pre_X = x = post_X = x_koo = None
            pre_Y = y = post_Y = y_koo = None
            koords_used = True

        #Is any element ending, so we can start to print again?
        if(verortungselement_ende.search(line)):
            elem = None
            koords_used = False
        elif(koordinaten_ende.search(line)):
            elemKO = None
            x_koo = None
            y_koo = None

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
