#!/usr/bin/env python3

from lxml.etree import XMLParser, parse
from fileinput import FileInput
from re import compile
from functools import reduce
from os import makedirs

import glob

patterns = [(compile(r'http://'), r'https://'),
            (compile(r'"https://(?:(?!/EP).)+/EP(?P<episode>(?:(?!\.mp3").)+)\.mp3"'), r'"https://traffic.libsyn.com/escapepod/EP\g<episode>.mp3"'),
            (compile(r'"https://[^"]+/podcast-mini4\.gif"'), r'"https://escapepod.org/wp-images/podcast-mini4.gif"')]

def load_episodes(feed, from_dir):
    episodes = sorted(glob.glob(from_dir + '/*.xml', recursive=True), reverse=True)
    for ep in episodes:
        print(ep)
        feed.append(parse(ep, XMLParser(strip_cdata=False)).getroot())

def replace(text):
    return reduce(lambda t, pattern: pattern[0].sub(pattern[1], t), patterns, text)

if __name__ == "__main__":
    generated_file = 'generated/feeds/escapepod.xml'
    makedirs('generated/feeds', exist_ok=True)

    feed = parse('original/escapepod/shell.xml', XMLParser(strip_cdata=False))

    channel = feed.getroot().find('./channel')
    load_episodes(channel, 'generated/escapepod/episodes/**')
    feed.write(generated_file)

    with FileInput(generated_file, inplace=True) as file:
        for index, line in enumerate(file):
            if index > 0:
                print(replace(line), end='')
            else:
                print(line)
