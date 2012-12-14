"""
The Watcher Watches Watchers.
"""

from apetools.baseclass import BaseClass
from apetools.commons.errors import CommandError


class TheWatcherError(CommandError):
    """
    """
# end class TheWatcherError


class TheWatcher(BaseClass):
    """
    The Watcher is a class to hold other watchers so you don't have to call start on all of them
    """
    def __init__(self, watchers, event=None, *args, **kwargs):
        """
        :param:

         - `watchers`: A collection of watchers.
         - `event`: An event shared by the threads.
        """
        super(TheWatcher, self).__init__(*args, **kwargs)
        self.watchers = watchers
        self.event = None
        self.threads = None
        return
        
    def start(self):
        """
        Starts all the watchers.

        :postcondition: self.threads is a list of started threads
        """
        try:
            self.threads = [watcher.start() for watcher in self.watchers]
        except AttributeError:
            raise TheWatcherError("No Watchers to Watch")
        return

    def stop(self):
        """
        If an event was provided in the constructor, sets it

        This assumes that the threads are using the event to check whether to commit suicide.
        """
        if self.event is not None:
            self.event.set()
        return

    def __call__(self, parameters=None, filename_prefix=None):
        """
        The main interface

        :param:

         - `parameters`: not used

        :postcondition: self.start called
        """
        self.start()
        return

    def __del__(self):
        """
        :postcondition: stop() called
        """
        self.stop()
        return
# end class TheWatcher
