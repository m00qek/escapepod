#!/usr/bin/env python3

from lxml.etree import XMLParser, parse
from fileinput import FileInput
from re import compile
from functools import reduce

import glob

patterns = [(compile(r'http://'), r'https://'),
            (compile(r'"https://(?:(?!/EP).)+/EP(?P<episode>(?:(?!\.mp3").)+)\.mp3"'), r'"https://traffic.libsyn.com/escapepod/EP\g<episode>.mp3"'),
            (compile(r'"https://[^"]+/podcast-mini4\.gif"'), r'"https://escapepod.org/wp-images/podcast-mini4.gif"')]

def load_episodes(feed, from_dir):
    episodes = sorted(glob.glob(from_dir + '/*.xml'))
    for ep in episodes:
        feed.append(parse(ep, XMLParser(strip_cdata=False)).getroot())

def replace(text):
    return reduce(lambda t, pattern: pattern[0].sub(pattern[1], t), patterns, text)

if __name__ == "__main__":
    generated_file = 'generated/feeds/old-episodes.xml'

    feed = parse('original/shell.xml', XMLParser(strip_cdata=False))

    channel = feed.getroot().find('./channel')
    load_episodes(channel, 'generated/episodes/rss-1')
    load_episodes(channel, 'generated/episodes/rss-2')

    feed.write(generated_file)

    with FileInput(generated_file, inplace=True) as file:
        for line in file:
            print(replace(line), end='')
