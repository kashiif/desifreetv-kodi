
import os
import sys
import xbmc
import xbmcgui
import urllib2
import xbmcaddon

from logger import KodiAddonLogger
import kodiaddonutils

from desifreetvviews import *

import desifreetvlistprovider

_logger = KodiAddonLogger.get_instance()
_logger.set_log_level('info')
_settings = kodiaddonutils.settings


def run():

    if sys.argv[2]:
        #_logger.debug('sys.argv[2]: ', sys.argv[2])
        params = kodiaddonutils.parse_query(sys.argv[2])
        _logger.debug('params: ', params)

        page_type = params.get('pagetype')

        if page_type == 'channel-list':
            _show_channel_menu(params)
        elif page_type == 'channel-show':
            _show_episodes_menu(params)
        elif page_type == 'show-episode':
            _show_episode(params)
    else:
        _show_main_menu()


def _show_main_menu():
    view = DesiFreeTvFolderListView()
    view.show(desifreetvlistprovider.fetch_channels_list())


def _show_episodes_menu(params):

    show_name = params.get('title')
    episodes_list = desifreetvlistprovider.fetch_episodes(params)

    _logger.debug('Listing episodes for ', show_name)

    view = DesiFreeTvFolderListView()
    view.show(episodes_list)


def _show_episode(params):

    title = params.get('title')
    title = urllib2.unquote(title)

    available_sources = desifreetvlistprovider.fetch_episode_sources(params)

    _logger.debug('Listing sources for ', available_sources)

    url_to_play = available_sources.get('dailymotion').get('urls')
    url_to_play = url_to_play[0]

    print 'url_to_play: %s' % url_to_play, title

    if url_to_play:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
        listitem.setInfo('Video', {'Title': title})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(url_to_play,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)


def _show_channel_menu(params):

    channel_name = params.get('title')
    shows_list = desifreetvlistprovider.fetch_channel_shows(params)

    _logger.debug('Listing shows for ', channel_name)

    view = DesiFreeTvFolderListView()
    view.show(shows_list)


if __name__ == '__main__':
    run()
