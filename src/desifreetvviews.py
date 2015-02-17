import sys

import xbmc
import xbmcgui
import xbmcplugin

import kodiaddonutils

from logger import KodiAddonLogger
_logger = KodiAddonLogger.get_instance()
_settings = kodiaddonutils.settings


class DesiFreeTvViewBase:

    def __init__(self):
        pass

    # common function for adding folder items
    def add_folder_list_item(self, item_params={}, size=0):
        _logger.debug('addFolderListItem', item_params)

        title = item_params.get('title')
        path = item_params.get('path')

        icon = kodiaddonutils.DEFAULT_FOLDER_IMAGE
        if icon:
            icon = kodiaddonutils.getThumbnail(icon)

        thumbnail = item_params.get('thumbnail', kodiaddonutils.DEFAULT_FOLDER_IMAGE)

        if thumbnail.find('http://') < 0:
            thumbnail = kodiaddonutils.getThumbnail(thumbnail)

        listitem = xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=thumbnail)
        url = '%s?path=%s&' % (sys.argv[0], path)
        url = kodiaddonutils.build_item_url(item_params, url)

        listitem.setProperty('Folder', 'true')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=True, totalItems=size)
        _logger.debug('addFolderListItem Done')

    # common function for adding video items
    def addChannelListItem(self, params={}, item_params={}, listSize=0):
        _logger.debug('addChannelListItem')

        icon = item_params.get('icon', 'live')
        icon = kodiaddonutils.getThumbnail(icon)
        title = item_params.get('title')
        thumbnailImage = item_params.get('thumbnail')

        listitem = xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=thumbnailImage)

        url = '%s?pagetype=channel&path=%s' % (sys.argv[0], item_params.get('path'))

        menu_items = []

        all_sources = item_params.get('sources')
        for source_key in all_sources:
            source_list = all_sources[source_key]

            item_url = '%s?pagetype=channel&path=%s%s' % (sys.argv[0], item_params.get('path'), '&streamid=%s')

            x = 0
            for stream in source_list:
                stream_id = '%s_%s' % (source_key, x)
                menu_title = 'Play Stream %s' % stream_id
                menu_path = item_url % stream_id
                menu_items.append((menu_title, menu_path))
                x += 1

        if len(menu_items) > 0:
            listitem.addContextMenuItems(menu_items, replaceItems=False)


        # cm = self.addVideoContextMenuItems(params, item_params)

        # listitem.addContextMenuItems(cm, replaceItems=True)

        # listitem.setProperty('Video', 'true')
        # listitem.setProperty('IsPlayable', 'true')
        listitem.setProperty('Genre', 'Live TV')
        # listitem.addStreamInfo('video', {'duration': item('Duration')})
        #listitem.setInfo(type='Video', infoLabels=item_params)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=False, totalItems=listSize + 1)
        _logger.debug('addVideoListItem Done')

    def set_video_mode(self):
        video_view = (_settings.getSetting('list_view') == '1')

        if video_view:
            xbmc.executebuiltin('Container.SetViewMode(500)')


class DesiFreeTvFolderListView(DesiFreeTvViewBase):

    def __init__(self):
        DesiFreeTvViewBase.__init__(self)

    def show(self, entries_list):
        _logger.debug('Main View :: show')
        cache = True

        for entry in entries_list:
            self.add_folder_list_item(item_params=entry)

        self.set_video_mode()

        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True, cacheToDisc=cache)
        _logger.debug('Main View :: show Done')

