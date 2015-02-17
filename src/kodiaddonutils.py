import os
import sys
import urllib2
import urllib

_in_xbmc = True

try:
    import xbmc
    import xbmcaddon
except:
    from xbmcenv import *

from logger import KodiAddonLogger
_logger = KodiAddonLogger.get_instance()

ADDON_NAME = 'DesiFree.tv'
ADDON_ID = 'plugin.video.desifreetv'
settings = xbmcaddon.Addon(id=ADDON_ID)

THUMBNAIL_PATH = os.path.join(settings.getAddonInfo('path'), 'thumbnails')
DEFAULT_FOLDER_TITLE = 'DefaultFolder'
DEFAULT_FOLDER_IMAGE = 'DefaultFolder.png'


def lang(string_id):
    return settings.getLocalizedString(string_id)

def getThumbnail(title):
    if not title:
        title = DEFAULT_FOLDER_TITLE

    thumbnail = os.path.join(ADDON_NAME, title + '.png')

    if not xbmc.skinHasImage(thumbnail):
        thumbnail = os.path.join(THUMBNAIL_PATH, title + '.png')
        if not os.path.isfile(thumbnail):
            thumbnail = DEFAULT_FOLDER_IMAGE

    return thumbnail


def build_item_url(item_params={}, url=''):
    blacklist = ('path', 'thumbnail', 'Overlay', 'icon', 'next', 'content', 'editid', 'summary', 'published', 'count',
                 'Rating', 'Plot', 'title', 'new_results_function', 'handler_class')
    for key, value in item_params.items():
        if key not in blacklist:
            url += key + '=' + value + '&'
    return url


def parse_query(query):

    params = {}
    if query[0] == '?':
        query = query[1:]

    # TODO: decode query
    all_vars = query.split('&')

    for item in all_vars:
        pair = item.split('=')
        params[pair[0]] = pair[1]

    return params


def fetch_url(url, headers={}, data=None):

    response = None
    response_text = None

    try:
        req = urllib2.Request(url)

        for key, value in headers.iteritems():
            req.add_header(key, value)

        if data:
            data = urllib.urlencode(data)

        response = urllib2.urlopen(req, data)
        response_text = response.read()

    finally:
        if response:
            try:
                response.close()
            except Exception:
                # ignore can't be done much about it
                pass

    return response_text


def get_profile_dir_path():
    return xbmc.translatePath(settings.getAddonInfo('profile'))

def get_plugin_dir_path():
    return xbmc.translatePath(settings.getAddonInfo('path'))
