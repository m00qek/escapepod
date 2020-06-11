#!/usr/bin/env python3
from lxml.etree import ElementTree, XMLParser, parse
from tempfile import TemporaryDirectory
from collections import OrderedDict
from shutil import copyfile, rmtree
from os import makedirs

import glob

def to_filename(title):
    return title.replace('/', '-')

def save_podcast(to_dir, prefix, xml):
    title = xml.findall('./title')[0]
    filename = '{0}/{1} -- {2}.xml'.format(to_dir, prefix, to_filename(title.text))
    ElementTree(xml).write(filename)

def split_feed(to_dir, file_index, file):
    root = parse(file, XMLParser(strip_cdata=False)).getroot()
    for index, item in enumerate(root.findall('./channel/item'), start=1):
        save_podcast(to_dir, '{0:03d} - {1:03d}'.format(file_index, index), item)

def split_all_feeds(from_dir, to_dir):
    files = sorted(glob.glob(from_dir + '/*.snapshot', recursive=True), reverse=True)
    for index, file in enumerate(files, start=1):
        split_feed(to_dir, index, file)

def load_with_guid(file):
    episode = parse(file, XMLParser(strip_cdata=False))
    guid = episode.getroot().findall('./guid')[0]
    return (guid.text, episode)

def title(episode):
    return episode.findall('./title')[0].text


def deduplicate_episodes(from_dir, to_dir):
    files = glob.glob(from_dir + '/*.xml', recursive=True)
    episodes = map(lambda ep: load_with_guid(ep), files)
    for index, ep in enumerate(OrderedDict(episodes).values(), start=1):
        new_file = '{0}/{1:03d} - {2}'.format(to_dir, index, to_filename(title(ep.getroot())) + '.xml' )
        print(new_file)
        ep.write(new_file)

def split(from_dir, to_dir):
    with TemporaryDirectory() as tmp_dir:
        split_all_feeds(from_dir, tmp_dir)
        rmtree(to_dir, ignore_errors=True)
        makedirs(to_dir, exist_ok=True)
        deduplicate_episodes(tmp_dir, to_dir)

if __name__ == "__main__":
    split('original/escapepod/feeds.feedburner.com/**', 'generated/escapepod/episodes/rss-1')
    split('original/escapepod/escapepod.org/**',        'generated/escapepod/episodes/rss-2')
