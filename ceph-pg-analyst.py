#!/usr/bin/env python
# requires: numpy, matplotlib
# complies with PEP 008
# written in python 2.7, however a library called 2to3
# allows this program to be run on python 3.x
from sys import argv  # imports argv from sys module
from sys import exit
from collections import Counter  # imports Counter from collections module
from json import load  # imports load from the json module
import numpy  # imports the entire numpy module
import matplotlib.pyplot as plt  # imports pyplot from matplotlib, calls at plt
from imp import find_module  # imports find_module from imp
import os # imports the entire os module as several functions are used
from shutil import rmtree

def statprint():
    val = pg_per_host.values()  # sets val to a list of the values in pg_per_host
    mean = numpy.mean(val)
    maxvalue = numpy.amax(val)
    minvalue = numpy.amin(val)
    std = numpy.std(val)
    median = numpy.median(val)
    variance = numpy.var(val)
    print "for placement groups on hosts: "
    print "the mean is: ", mean
    print "the max value is: ", maxvalue
    print "the min value is: ", minvalue
    print "the standard deviation is: ", std
    print "the median is: ", median
    print "the variance is: ", variance
    # prints statements for stats
    host_mean = numpy.mean(host_per_pg)
    host_max = numpy.amax(host_per_pg)
    host_min = numpy.amin(host_per_pg)
    host_std = numpy.std(host_per_pg)
    host_median = numpy.median(host_per_pg)
    host_variance = numpy.var(host_per_pg)
    # these are the variables for hosts/pgs
    print "hosts per placement group: "
    print "the mean is: ", host_mean
    print "the max value is: ", host_max
    print "the min value is: ", host_min
    print "the standard deviation is: ", host_std
    print "the median is: ", host_median
    print "the variance is: ", host_variance


def pgpf():
    for pg in pf:
        pg_hosts = set()
        for osd in pg:
            hostname = osd2host[osd]
            pg_per_host[hostname] += 1
            pg_hosts.add(hostname)
        host_per_pg.append(len(pg_hosts))
        
def h_in_hosts():
        for h in hosts:
            name = h['name']
            for c in h['children']:
                osd2host[c] = name
        
try:
    find_module('numpy')  # makes sure numpy is installed
    find_module('matplotlib')  # makes sure matplotlib is installed
    foundmodule = True  # sets foundmodule to boolean True
except ImportError:  # if there is an importerror, one module isnt installed
    foundmodule = False  # sets foundmodule to boolean False
module_error_message = ("You dont appear to have either numpy \
 or matplotlib installed. The program will not work without these.\
 please press ctrl+D to finish")  # string with error message
if foundmodule == False:  # if the foundmodule is anything but True
    print(module_error_message)  # outputs the error message string
else:
    pass  # otherwise, code continues running
    
# if needs scrapping delete from here
if len(argv) == 4:
    i = 1
    for item in argv[1:3]:
        with open(item) as pfg: 
            pf = map(eval, map(str.strip, pfg.readlines()))
    
        hosts = {}  
        if i == 1:
            with open(argv[3]) as treefile:
                 tree = load(treefile)
   
        hosts = filter(lambda x: True if x['type'] == 'host' else False, tree['nodes'])

        osd2host = {}  
        h_in_hosts()
                
        pg_per_host = Counter()
        host_per_pg = []

        pgpf()
            
        # stats on pgs per host
        print
        print
        print item[-6:]
        statprint()
        i += 1
    exit(-1)           
else: 
    pass
# to here

with open(argv[1]) as pfg:  # uses the second argument in the command line
    pf = map(eval, map(str.strip, pfg.readlines()))
    # opens a plain text file which has all the PGs in according to OSD names
    # this is then mapped and evaluated and is stored as a list of lists.

hosts = {}  # empty dictionary

with open(argv[2]) as treefile:
    tree = load(treefile)
    # second command line argument should be a JSON treefile
hosts = filter(lambda x: True if x['type'] == 'host' else False, tree['nodes'])
# filters out the host and nodes to be stored as keypairs in the host
# dictionary which was assigned earlier
osd2host = {}  # empty dictionary

h_in_hosts()

    # osd2host = { c: name for c in h['children'] }
    # loops though hosts and assigns keys and values
pg_per_host = Counter()
host_per_pg = []
# pg_per_host is assigned to a counter, which is from the collections module
# host_per_pg is assigned to a blank list

pgpf()
    # pg_hosts is a set so no values are duplicated because this is looking
    # at unique host names rather than doubled up ones.

# stats on pgs per host
print
print
print argv[1][-6:]
statprint()

try: 
    hist_opt = argv[4]
    file_name = argv[5]
except:
    pass
if len(argv) == 3:
    if 'DISPLAY' in os.environ:
        plt.hist(host_per_pg)
        title_hist = "Hosts per pg histogram on", argv[1][-6:]
        plt.title(title_hist)
        plt.xlabel("No. of hosts")
        plt.ylabel("Frequency")
        plt.show()
    else:
        print("You do not have a display manager installed \
        use the -h tag at the end of the script to save a picture\
        of the histogram to your local directory unless specified \
        otherwise. ")
elif hist_opt == '-h':
    matplotlib.use('Agg')
    plt.hist(host_per_pg)
    title_hist = "Hosts per pg histogram on", argv[1][-6:]
    plt.title(title_hist)
    plt.xlabel("No. of hosts")
    plt.ylabel("Frequency")
    fig = plt.figure()
    fig.savefig(file_name)
else:
   pass


