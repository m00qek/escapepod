#!/usr/bin/env python3

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
