

class xbmc:
    @staticmethod
    def translatePath(path):
        return 'D:\\Temp'


class xbmcaddon:

    @staticmethod
    def Addon(id=''):
        return xbmcsettings()


class xbmcsettings:

    def getAddonInfo(self, name):
        return ''

