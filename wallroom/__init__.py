import os
import re
from argparse import ArgumentParser

import requests
from requests_html import HTMLSession

from .__version__ import __version__

base_url = r'https://wallroom.io'


def cli():
    parser = ArgumentParser()
    parser.add_argument()


def get_sizes():
    resolutions = set()
    session = HTMLSession()
    r = session.get(base_url)
    nav = r.html.find('.nav-bundles', first=True)
    for size_group in nav.links:
        if size_group in {'/', '/new'}:
            continue
        r = session.get(base_url + size_group)
        res_nav = r.html.find('.nav-resolutions', first=True)
        resolutions.update([res.strip('/') for res in res_nav.links])
    return resolutions


def get_images(size):
    images = []
    session = HTMLSession()
    r = session.get(base_url + '/' + size)
    img_links = r.html.find('.image-list a')
    for link in img_links:
        images.append(link.attrs['href'])
    return images


def download_images(size, directory=None, n=10):
    if not directory:
        directory = os.path.expanduser('~/wallroom')
    if not os.path.exists(directory):
        os.makedirs(directory)

    downloaded_images = set()
    for fn in os.listdir(directory):
        fp = os.path.join(directory, fn)
        if os.path.isfile(fp):
            downloaded_images.add(os.path.splitext(fn)[0])

    images = get_images(size)
    for i, image in enumerate(images):
        if n is not None and i >= n:
            return
        size, id = image.strip('/').split('/')
        filename = 'wallroom-{size}-{id}'.format(size=size, id=id)
        if filename in downloaded_images:
            continue
        url = base_url + image + '/download'
        r = requests.get(url)
        fn = re.match(r'attachment; filename=(.+)$', r.headers['Content-Disposition']).group(1)
        ext = os.path.splitext(fn)[1]
        filepath = os.path.join(directory, filename + ext)
        with open(filepath, 'wb') as f:
            f.write(r.content)
