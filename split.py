#!/usr/bin/env python3
from lxml.etree import ElementTree, XMLParser, parse
from tempfile import TemporaryDirectory
from collections import OrderedDict
from shutil import copyfile, rmtree
from os import mkdir

import glob

def title_to_filename(title):
    return title.replace('/', '-')

def save_podcast(to_dir, prefix, xml):
    title = xml.findall('./title')[0]
    filename = '{0}/{1} -- {2}.xml'.format(to_dir, prefix, title_to_filename(title.text))
    ElementTree(xml).write(filename)

def split_feed(to_dir, file_index, file):
    root = parse(file, XMLParser(strip_cdata=False)).getroot()
    for index, item in enumerate(root.findall('./channel/item'), start=1):
        save_podcast(to_dir, '{0:02d} - {1:02d}'.format(file_index, index), item)

def split_all_feeds(from_dir, to_dir):
    files = sorted(glob.glob(from_dir + '/*.xml'), reverse=True)
    for index, file in enumerate(files, start=1):
        split_feed(to_dir, index, file)

def deduplicate_episodes(from_dir, to_dir):
    allfiles = sorted(glob.glob(from_dir + '/*.xml'), reverse=True)
    episodes = map(lambda ep: (ep.split(' -- ')[1], ep), allfiles)
    for index, (name, filename) in enumerate(OrderedDict(episodes).items(), start=1):
        copyfile(filename, '{0}/{1:03d} - {2}'.format(to_dir, index, name))

def split(from_dir, to_dir):
    with TemporaryDirectory() as tmp_dir:
        split_all_feeds(from_dir, tmp_dir)
        rmtree(to_dir, ignore_errors=True)
        mkdir(to_dir)
        deduplicate_episodes(tmp_dir, to_dir)

if __name__ == "__main__":
    mkdir('generated/episodes')
    split('original/feeds/rss-2', 'generated/episodes/rss-2')
    split('original/feeds/rss-1', 'generated/episodes/rss-1')
