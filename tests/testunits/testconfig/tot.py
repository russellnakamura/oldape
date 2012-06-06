output = """
[DEFAULT]
# the DEFAULT section is where you create variables
# that can be used in later sections
control_network = 192.168.10
test_network = 192.168.20

[TEST]
output_folder = data_{t}
# The data files will be appended with .iperf
data_file = %(output_folder)s
# This is the number of times to repeat the throughput test
repetitions = 1

[DUT]
test_ip_address = %(test_network)s.70

[TRAFFIC_PC]
control_ip_address = %(control_network)s.50
test_ip_address = %(test_network)s.50

login = allion
# if you have ssh-keys set up you can leave the password commented out
#password=

[IPERF]
# The names of the options should conform to the long-format options
# e.g. -P would be `parallel`

# this is the -t flag: (n) [seconds | minutes | hours | days]
time = 10 seconds

# **** the following are Allion's defaults ****
# you shouldn't have to change them

# tcp window size
# this is the -w flag: n[KM]
window = 256K

# buffer-length
#this is the -l flag: (n)
length = 1470

# Parallel Threads
# This is the -P flag: (n)
parallel = 4

# time between data reports
# this is the -i flag: (n) 
interval = 1

# Data Units
# this is the -f flag: b|k|m|K|M
format = m
"""


output_folder = "data_{t}"
data_file = output_folder
dut_test_ip_address = "192.168.20.70"
tpc_control_ip_address = "192.168.10.50"
tpc_test_ip_address = "192.168.20.50"

tcp_window_size = "256K"
buffer_length = "1470"
parallel_threads = "4"
data_intervals = "1"
data_units = "m"
test_duration = "10"
