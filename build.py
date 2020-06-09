#!/usr/bin/env python3

from lxml.etree import XMLParser, parse
from fileinput import FileInput
from re import compile

import glob

regex = compile(r'https://.*/EP(?P<episode>.+)\.mp3')

def load_episodes(feed, from_dir):
    episodes = sorted(glob.glob(from_dir + '/*.xml'))
    for ep in episodes:
        feed.append(parse(ep, XMLParser(strip_cdata=False)).getroot())

def use_https(text):
    return text.replace('http://', 'https://')

def renew_links(text):
    return regex.sub(r'https://traffic.libsyn.com/escapepod/EP\g<episode>.mp3', text)

if __name__ == "__main__":
    feed = parse('shell.xml', XMLParser(strip_cdata=False))

    channel = feed.getroot().find('./channel')
    load_episodes(channel, 'episodes/rss-1')
    load_episodes(channel, 'episodes/rss-2')

    feed.write('feeds/generated/all.xml')

    with FileInput('feeds/generated/all.xml', inplace=True) as file:
        for line in file:
            print(renew_links(use_https(line)), end='')
