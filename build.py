#!/usr/bin/env python3

from collections import OrderedDict
from lxml.etree import ElementTree, XMLParser, parse, fromstring, tostring
from functools import reduce
from glob import glob
from os import makedirs

import re

DEFAULT_REPLACEMENTS = [(re.compile(r'http://'), r'https://'),
                        (re.compile(r'xmlns:(?P<ns>[^=]+)="https://'), r'xmlns:\g<ns>="http://')]

def load_xml_from_file(file):
    return parse(file, parser=XMLParser(strip_cdata=False))

def load_xml_from_text(text):
    return fromstring(text, parser=XMLParser(strip_cdata=False))

def xml_to_text(xml):
    return tostring(xml, encoding='unicode')


def load_episodes(episodes, from_dir):
    files = sorted(glob(from_dir), reverse=True)
    guid = lambda episode: episode.findall('./title')[0].text

    for file in files:
        feed = load_xml_from_file(file)

        for episode in feed.getroot().findall('./channel/item'):
            episodes[guid(episode)] = episode

def replace_all(replacements, episode):
    replace = lambda text, pattern: pattern[0].sub(pattern[1], text)
    all_replacements = DEFAULT_REPLACEMENTS + replacements

    modified_text = reduce(replace, all_replacements, xml_to_text(episode))

    return load_xml_from_text(modified_text)

def build(from_directories, replacements, shell_file, to_file):
    episodes = OrderedDict()

    for from_dir in from_directories:
        load_episodes(episodes, from_dir)

    feed = load_xml_from_file(shell_file)
    channel = feed.getroot().find('./channel')
    for episode in episodes.values():
        channel.append(replace_all(replacements, episode))

    feed.write(to_file)


if __name__ == "__main__":
    makedirs('generated', exist_ok=True)

    #Escape Pod
    build(['original/escapepod/escapepod.org/feed/*.snapshot',
           'original/escapepod/feeds.feedburner.com/escapepod/*.snapshot'],
          [(re.compile(r'"https://(?:(?!/EP).)+/EP(?P<episode>(?:(?!\.mp3").)+)\.mp3"'), r'"https://traffic.libsyn.com/escapepod/EP\g<episode>.mp3"'),
           (re.compile(r'"https://[^"]+/podcast-mini4\.gif"'), r'"https://escapepod.org/wp-images/podcast-mini4.gif"')],
          'original/escapepod/shell.xml',
          'generated/escapepod.rss')

