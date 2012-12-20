from unittest import TestCase
import time
from StringIO import StringIO

from mock import MagicMock, patch, call, PropertyMock

from apetools.watchers.procnetdevwatcher import ProcnetdevWatcher, ProcnetdevWatcherEnum, HEADER
from apetools.watchers.procnetdevwatcher import REXPRESSION_KEYS
from apetools.commons.timestamp import TimestampFormat

sample = """
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo:   52989     577    0    0    0     0          0         0    52989     577    0    0    0     0       0          0
 wlan0:   27035     223    0    0    0     0          0         0    34708     301    0    0    0     0       0          0
wlan0-mon: 15683751  116759    0    0    0     0          0         0        0       0    0    0    0     0       0          0
  eth0: 78917734   69440    0    0    0     0          0       334  4920158   33266    0    0    0     0       0          0
"""

line = "wlan0-mon: 15683751  116759    12    13    14     15          0         0        16       17    18    19    20     21       22          0"
interface = 'wlan0-mon'

sample2 = """
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo:   52989     577    0    0    0     0          0         0    52989     577    0    0    0     0       0          0
 wlan0:   27035     223    0    0    0     0          0         0    34708     301    0    0    0     0       0          0
wlan0-mon: 15683752  116761    3    4    5     6          0         0        7       8    9    10    11     12       13          0
  eth0: 78917734   69440    0    0    0     0          0       334  4920158   33266    0    0    0     0       0          0
"""

OUTPUT = ",".join('1 2 3 4 5 6 7 8 9 10 11 12 13'.split()) + "\n"
TIMESTAMP = '2012-12-17:13:46:26'

class TestProcnetdevWatcher(TestCase):
    def setUp(self):
        self.output = MagicMock()
        self.connection = MagicMock()
        self.timestamp = MagicMock()
        self.watcher = ProcnetdevWatcher(output=self.output, interface=interface,
                                         connection = self.connection,
                                         interval=1)
        self.watcher._timestamp = self.timestamp
        return

    def test_keys(self):
        self.assertEqual(REXPRESSION_KEYS[0], ProcnetdevWatcherEnum.receive_bytes)
        return

    def test_expression(self):
        match = self.watcher.expression.search(line).groupdict()
        self.assertIsNotNone(match)
        self.assertEqual("15683751", match[ProcnetdevWatcherEnum.receive_bytes])
        self.assertEqual("116759", match[ProcnetdevWatcherEnum.receive_packets])
        self.assertEqual('wlan0-mon', match[ProcnetdevWatcherEnum.interface])
        self.assertEqual("12", match[ProcnetdevWatcherEnum.receive_errs])
        self.assertEqual("13", match[ProcnetdevWatcherEnum.receive_drop])
        self.assertEqual("14", match[ProcnetdevWatcherEnum.receive_fifo])
        self.assertEqual('15', match[ProcnetdevWatcherEnum.receive_frame])
        
        self.assertEqual('16', match[ProcnetdevWatcherEnum.transmit_bytes])
        self.assertEqual('17', match[ProcnetdevWatcherEnum.transmit_packets])
        self.assertEqual('18', match[ProcnetdevWatcherEnum.transmit_errs])
        self.assertEqual('19', match[ProcnetdevWatcherEnum.transmit_drop])
        self.assertEqual('20', match[ProcnetdevWatcherEnum.transmit_fifo])
        self.assertEqual('21', match[ProcnetdevWatcherEnum.transmit_colls])
        self.assertEqual('22', match[ProcnetdevWatcherEnum.transmit_carrier])
        return

    def test_stop(self):
        self.assertFalse(self.watcher.stopped)        
        self.watcher.stop()
        self.assertTrue(self.watcher.stopped)
        return

    def test_call(self):
        output = [(StringIO(sample),""), (StringIO(sample2), "")]
        def side_effects(*args, **kwargs):
            return output.pop(0)
        
        self.connection.cat.side_effect = side_effects
        timer = MagicMock()
        expected = [call.write(HEADER), call.write(OUTPUT)]
        self.timestamp.now.return_value = TIMESTAMP
        
        with patch('time.time', timer):
            with patch('apetools.commons.timestamp.TimestampFormat.now', new_callable=PropertyMock) as mock_now:
                mock_now.__get__ = MagicMock(return_value = TIMESTAMP)
                self.watcher._timestamp = None
                self.watcher.start()
                time.sleep(1)
                self.watcher.stop()
        calls = self.output.write.call_args_list
        self.assertEqual(expected, calls)
# end class TestProcnetdevWatcher

class TestTimestampFormat(TestCase):
    def setUp(self):
        self.format = TimestampFormat()
        return

    def test_iperf_format(self):
        return
# end class TestTimestampFormat
