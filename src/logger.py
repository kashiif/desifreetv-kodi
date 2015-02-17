
_logger = None

class KodiAddonLogger:

    def __init__(self):
        self.__log_level = 'info'

    def set_log_level(self, log_level):
        if log_level not in ['debug', 'info', 'warn', 'error']:
            pass
        self.__log_level = log_level

    @staticmethod
    def get_instance():
        global _logger
        if _logger is None:
            _logger = KodiAddonLogger()

        return _logger

    def __print(self, log_level, *args):
        if log_level != self.__log_level:
            return

        print 'Desi-Kodi :: %s' % str(args)

    def debug(self, *args):
        self.__print('debug', args)

    def log(self, *args):
        self.__print('log', args)

    def warn(self, *args):
        self.__print('warn', args)

    def error(self, *args):
        self.__print('error', args)
