#!/usr/bin/env python3

from fileinput import FileInput
import xml.etree.ElementTree as ET
import glob

def load_episodes(feed, from_dir):
    episodes = sorted(glob.glob(from_dir + '/*.xml'))
    for ep in episodes:
        feed.append(ET.parse(ep).getroot())

if __name__ == "__main__":
    feed = ET.parse('shell.xml')

    channel = feed.getroot().find('./channel')
    load_episodes(channel, 'episodes/rss-1')
    load_episodes(channel, 'episodes/rss-2')

    feed.write('feeds/generated/all.xml')

    with FileInput('feeds/generated/all.xml', inplace=True) as file:
        for line in file:
            print(line.replace('http://', 'https://'), end='')
