"""
A class to talk to an oscillator.
"""

#python standard library
from threading import Thread, Event
from Queue import Queue

# apetools modules
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConnectionError, CommandError
from apetools.commons.timestamp import TimestampFormat
from basecommand import BaseThreadedCommand

class OscillatorError(CommandError):
    """
    """
# end class OscillatorError

class Oscillate(BaseThreadedCommand):
    """
    A Class to start and stop an oscillator
    """
    def __init__(self, connection, output, arguments, block=False):
        """
        :param:

         - `connection`: connection to oscillation master
         - `output`: file to send angle information to
         - `arguments`: string of arguments for the oscillate command
         - `block`: if True, waits for rotation start on each call
        """
        super(Oscillate, self).__init__()
        self.connection = connection
        self.output = output
        self.block = block
        self._timestamp = None
        self.arguments = arguments
        self._rotation_start = None
        self._event = None
        self._thread = None
        self._error_queue = None
        return

    @property
    def event(self):
        """
        :return: OscillateEvent with self.rotation_start event
        """
        if self._event is None:
            self._event = OscillateEvent(self.rotation_start)
        return self._event

    @property
    def timestamp(self):
        """
        :return: timestamper
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat()
        return self._timestamp
        

    @property
    def error_queue(self):
        """
        :return: queue of error messages
        """
        if self._error_queue is None:
            self._error_queue = Queue()
        return self._error_queue

    @property
    def rotation_start(self):
        """
        :return: threading event
        """
        if self._rotation_start is None:
            self._rotation_start = Event()
        return self._rotation_start

    @property
    def thread(self):
        """
        :return: self.run executing in a thread       
        """
        if self._thread is None:
            self._thread = Thread(target=self.run, name="Oscillator")
            self._thread.daemon = True
            self._thread.start()
        return self._thread
    
    def run(self):
        """
        :postcondition: oscillate command sent to the oscillator
        """
        try:
            with self.connection.lock:
                output, error = self.connection.oscillate(self.arguments)
            for line in self.generate_output(output, error):            
                self.logger.debug(line)
                if line.startswith("<Oscillator>"):
                    self.output.write("{0}:{1}".format(self.timestamp.now, line))
                    continue
                if line.startswith("Rotating from"):
                    self.rotation_start.set()
                    continue

        except Exception as error:
            self.error_queue.put(error)
        self.check_error(error)
        return

    def check_error(self, error):
        """
        Not fully implented yet.

        :param:

         - `error`: stderr file
       
        :raise: CommandError if detected
        """
        line = error.readline()
        if len(line):
            if "pthread_mutex_destroy" in line:
                self.error_queue.put(line)
                self.logger.warning("Unable to grab the lock: Is the Oscillator already running?")
            else:
                self.logger.warning(line)
        return

    def generate_output(self, output, error):
        """
        :param:

         - `output`: stdout file
         - `error`: stderr file
        :yield: lines of stdout
        """
        for line in output:
            yield line
        self.check_error(error)
        return
    
    def stop(self):
        """
        :postcondition:

         - `stopped` is True
         - pkill(`oscillate`) called
         - rotate() called
        """
        with self.connection.lock:
            for line in self.generate_output(*self.connection.pkill('oscillate;rotate 0 -k')):
                self.logger.debug(line)
        self.stopped = True
        return

    def __call__(self, parameter=None):
        """
        :param:

         - `parameter`: not used
         
        :postcondition: thread is running, rotation_start is set
        """
        if self.thread.is_alive():
            if self.block:
                self.event.wait()
        elif not self.error_queue.empty():
            raise OscillatorError("Unable to Oscillate: {0}".format(self.error_queue.get()))
        return

    def __del__(self):
        """
        :postcondition: `stop` is called.
        :postcondition: connection is closed
        """
        try:
            self.stop()
            #self.connection.client.close()
        except ConnectionError:
            self.logger.debug("Connection Already closed")
        return

# end class Oscillator

class OscillateEvent(BaseClass):
    """
    An event to coordinate other commands with the start of a rotation
    """
    def __init__(self, event):
        """
        :param:

         - `event`: a python Event
        """
        super(OscillateEvent, self).__init__()
        self.event = event
        return

    def wait(self):
        """
        :postcondition: event is cleared then waited for
        """
        self.event.clear()
        self.logger.info("Waiting for the start of the next rotation.")
        self.event.wait()
        return
# end class OscillateEvent
    

class OscillateStop(BaseClass):
    """
    A class to explicitly stop the Oscillator, since the Destructor doesn't seem to work.
    """
    def __init__(self, connection):
        """
        :param:

         - `connection`: a connection to the rotation master
        """
        super(OscillateStop, self).__init__()
        self.connection = connection
        return

    def kill_and_rotate(self):
        """
        :postcondition: pkill oscillate and rotate 0 -k sent to connection
        :return: True if on stderr output, False otherwise
        """
        with self.connection.lock:
            output, error = self.connection.pkill('oscillate;sleep 2;rotate 0 -k')

        for line in output:
            self.logger.info(line)
        err = error.readline()
        if len(err):
            self.logger.error(err)
            return False
        return True
    
    def __call__(self, parameter=None):
        """
        :param:

         - `parameter`: Not used
        
        :postcondition:
        """
        if not self.kill_and_rotate():
            self.logger.error("Sleeping 5 seconds and trying again.")
            self.kill_and_rotate()
        return
# end OscillateStop
