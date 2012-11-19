from tottest.parsers import iperfparser

from unittest import TestCase

EDGE = """
------------------------------------------------------------
Client connecting to 192.168.20.50, TCP port 5001
TCP window size: 16.0 KByte (default)
------------------------------------------------------------
[  3] local 192.168.20.62 port 33593 connected with 192.168.20.50 port 5001
[  4] local 192.168.20.62 port 33594 connected with 192.168.20.50 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec  1.00 MBytes  8.39 Mbits/sec
[  4]  0.0- 1.0 sec   896 KBytes  7.34 Mbits/sec
[SUM]  0.0- 1.0 sec  1.88 MBytes  15.7 Mbits/sec
[  3]  1.0- 2.0 sec   640 KBytes  5.24 Mbits/sec
[  4]  1.0- 2.0 sec   512 KBytes  4.19 Mbits/sec
[SUM]  1.0- 2.0 sec  1.12 MBytes  9.44 Mbits/sec
[  3]  2.0- 3.0 sec   512 KBytes  4.19 Mbits/sec
[  4]  2.0- 3.0 sec   512 KBytes  4.19 Mbits/sec
[SUM]  2.0- 3.0 sec  1.00 MBytes  8.39 Mbits/sec
[  4]  3.0- 4.0 sec   384 KBytes  3.15 Mbits/sec
[  3]  3.0- 4.0 sec   384 KBytes  3.15 Mbits/sec
[SUM]  3.0- 4.0 sec   768 KBytes  6.29 Mbits/sec
[  3]  4.0- 5.0 sec   512 KBytes  4.19 Mbits/sec
[  4]  4.0- 5.0 sec   768 KBytes  6.29 Mbits/sec
[SUM]  4.0- 5.0 sec  1.25 MBytes  10.5 Mbits/sec
[  4]  5.0- 6.0 sec   384 KBytes  3.15 Mbits/sec
[  3]  5.0- 6.0 sec   384 KBytes  3.15 Mbits/sec
[SUM]  5.0- 6.0 sec   768 KBytes  6.29 Mbits/sec
[  3]  6.0- 7.0 sec  0.00 Bytes  0.00 bits/sec
[  3]  7.0- 8.0 sec  0.00 Bytes  0.00 bits/sec
[  3]  8.0- 9.0 sec  0.00 Bytes  0.00 bits/sec
[  3]  9.0-10.0 sec  0.00 Bytes  0.00 bits/sec
[  3]  0.0-10.7 sec  3.50 MBytes  2.73 Mbits/sec
[  4]  6.0- 7.0 sec   256 KBytes  2.10 Mbits/sec
[SUM]  6.0- 7.0 sec   256 KBytes  2.10 Mbits/sec
[  4]  7.0- 8.0 sec  0.00 Bytes  0.00 bits/sec
[SUM]  7.0- 8.0 sec  0.00 Bytes  0.00 bits/sec
[  4]  8.0- 9.0 sec  0.00 Bytes  0.00 bits/sec
[SUM]  8.0- 9.0 sec  0.00 Bytes  0.00 bits/sec
[  4]  9.0-10.0 sec  0.00 Bytes  0.00 bits/sec
[SUM]  9.0-10.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 10.0-11.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 11.0-12.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 12.0-13.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 13.0-14.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 14.0-15.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 15.0-16.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 16.0-17.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 17.0-18.0 sec  0.00 Bytes  0.00 bits/sec
[  4] 18.0-19.0 sec  0.00 Bytes  0.00 bits/sec
[  4]  0.0-19.3 sec  3.75 MBytes  1.63 Mbits/sec
""".split("\n")

EDGECSV = """
20120720091543,192.168.20.62,33596,192.168.20.50,5001,4,0.0-1.0,393216,3145728
20120720091543,192.168.20.62,33595,192.168.20.50,5001,3,0.0-1.0,393216,3145728
20120720091543,192.168.20.62,0,192.168.20.50,5001,-1,0.0-1.0,786432,6291456
20120720091544,192.168.20.62,33595,192.168.20.50,5001,3,1.0-2.0,393216,3145728
20120720091544,192.168.20.62,33596,192.168.20.50,5001,4,1.0-2.0,524288,4194304
20120720091544,192.168.20.62,0,192.168.20.50,5001,-1,1.0-2.0,917504,7340032
20120720091544,192.168.20.62,33596,192.168.20.50,5001,4,2.0-3.0,917504,7340032
20120720091545,192.168.20.62,33595,192.168.20.50,5001,3,2.0-3.0,1048576,8388608
20120720091545,192.168.20.62,0,192.168.20.50,5001,-1,2.0-3.0,1966080,15728640
20120720091546,192.168.20.62,33595,192.168.20.50,5001,3,3.0-4.0,131072,1048576
20120720091547,192.168.20.62,33595,192.168.20.50,5001,3,4.0-5.0,655360,5242880
20120720091547,192.168.20.62,33596,192.168.20.50,5001,4,3.0-4.0,393216,3145728
20120720091547,192.168.20.62,0,192.168.20.50,5001,-1,3.0-4.0,524288,4194304
20120720091547,192.168.20.62,33596,192.168.20.50,5001,4,4.0-5.0,0,0
20120720091547,192.168.20.62,0,192.168.20.50,5001,-1,4.0-5.0,655360,5242880
20120720091549,192.168.20.62,33595,192.168.20.50,5001,3,5.0-6.0,655360,5242880
20120720091549,192.168.20.62,33595,192.168.20.50,5001,3,6.0-7.0,0,0
20120720091551,192.168.20.62,33595,192.168.20.50,5001,3,7.0-8.0,262144,2097152
20120720091552,192.168.20.62,33595,192.168.20.50,5001,3,8.0-9.0,131072,1048576
20120720091554,192.168.20.62,33596,192.168.20.50,5001,4,5.0-6.0,262144,2097152
20120720091554,192.168.20.62,0,192.168.20.50,5001,-1,5.0-6.0,917504,7340032
20120720091554,192.168.20.62,33596,192.168.20.50,5001,4,6.0-7.0,0,0
20120720091554,192.168.20.62,0,192.168.20.50,5001,-1,6.0-7.0,0,0
20120720091555,192.168.20.62,33595,192.168.20.50,5001,3,9.0-10.0,131072,1048576
20120720091555,192.168.20.62,33595,192.168.20.50,5001,3,0.0-14.0,3932160,2239342
20120720091556,192.168.20.62,33596,192.168.20.50,5001,4,7.0-8.0,131072,1048576
20120720091556,192.168.20.62,0,192.168.20.50,5001,-1,7.0-8.0,393216,3145728
20120720091556,192.168.20.62,33596,192.168.20.50,5001,4,8.0-9.0,0,0
20120720091556,192.168.20.62,0,192.168.20.50,5001,-1,8.0-9.0,131072,1048576
20120720091556,192.168.20.62,33596,192.168.20.50,5001,4,9.0-10.0,0,0
20120720091556,192.168.20.62,0,192.168.20.50,5001,-1,9.0-10.0,131072,1048576
20120720091556,192.168.20.62,33596,192.168.20.50,5001,4,10.0-11.0,0,0
20120720091556,192.168.20.62,33596,192.168.20.50,5001,4,11.0-12.0,0,0
20120720091556,192.168.20.62,33596,192.168.20.50,5001,4,0.0-14.8,2752512,1483421
20120720091556,192.168.20.62,0,192.168.20.50,5001,-1,0.0-14.8,6684672,3602594
""".split("\n")

INTERVALS = [float(i) for i in "0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0".split()]
BANDWIDTHS = "15.73 9.43 8.38 6.3 10.48 6.3 2.1 0.0 0.0 0.0".split()
BANDWIDTHS = [float(b) for b in BANDWIDTHS]

BANDWIDTHSCSV = [6.291456, 7.340032, 15.728640, 4.194304, 5.24288, 7.340032, 0,
                 3.145728, 1.048576, 1.048576, 0, 0, 0]
INTERVALSCSV = [float(i) for i in range(len(BANDWIDTHSCSV))]

class TestEdgeIperf(TestCase):
    def setUp(self):
        self.parser = iperfparser.IperfParser()
        return

    def test_bandwiths(self):
        for line in EDGE:
            self.parser(line)
        
        for index, interval in enumerate(INTERVALS):
            self.assertAlmostEqual(BANDWIDTHS[index], self.parser.intervals[interval])
        return

class TestEdgeIperfCSV(TestCase):
    def setUp(self):
        self.parser = iperfparser.IperfParser()
        return

    def test_bandwiths(self):
        self.parser.reset()
        for line in EDGECSV:
            self.parser(line)
        for index, interval in enumerate(INTERVALSCSV):
            self.assertAlmostEqual(BANDWIDTHSCSV[index], self.parser.intervals[interval])
        return
