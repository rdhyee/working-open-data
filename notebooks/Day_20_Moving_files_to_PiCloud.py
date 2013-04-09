# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <style media="screen" type="text/css">
#     body {color:blue;}
# </style>

# <headingcell level=1>

# Prerequisites

# <markdowncell>

# Although strictly speaking, you can do all the work directly on PiCloud (where I'm handling the dependencies), you'll likely want to get PiCloud, boto, s3cmd set up locally.  See [Day 19 notes](http://nbviewer.ipython.org/urls/raw.github.com/rdhyee/working-open-data/master/notebooks/Day_19_CC_etc.ipynb) and [Day 16 PiCloud intro](http://nbviewer.ipython.org/urls/raw.github.com/rdhyee/working-open-data/master/notebooks/Day_16_PiCloud_intro.ipynb) for a refresher.  **One big reason for working locally is that you'll get charged for the time you are running a PiCloud notebook server** -- and when you are thinking, it's nice to not have to worry about the time (even if it is $0.05/hour for a running a c1 PiCloud instance.)
# 
# Also ask for help if you are having problems.

# <headingcell level=1>

# Moving notebooks between local storage and PiCloud

# <markdowncell>

# Listing what's in your PiCloud bucket

# <codecell>

import cloud
cloud.bucket.list()

# <headingcell level=1>

# using cloud.bucket

# <headingcell level=2>

# copying from local computer to PiCloud using cloud.bucket.put

# <codecell>

# http://docs.picloud.com/moduledoc.html#module-cloud.bucket

import os
# only if we not running on picloud....
if not os.path.exists('/home/picloud/notebook'):
    pass
    # normally I keep this line commented to prevent accidental copying if I run the notebook through.
    cloud.bucket.put('Day_20_Moving_files_to_PiCloud.ipynb', prefix='notebook')

# <headingcell level=2>

# copying from PiCloud to local machine using cloud.bucket.get

# <codecell>

import os

if not os.path.exists('/home/picloud/notebook'):
    pass
    # normally I keep this line commented to prevent accidental copying if I run the notebook through.
    # note the new local name -- to make it less likely to overwrite something I'm doing locally.
    #cloud.bucket.get('notebook/Day_20_CommonCrawl.ipynb', 'Day_20_CommonCrawl_from_picloud.ipynb')

# <headingcell level=1>

# Using ssh

# <markdowncell>

# **Warning:** I don't think you'll immediately see the notebook changes reflected in an already running PiCloud notebook server -- at least, that was my experience.

# <markdowncell>

# There are other ways to interact with PiCloud -- using picloud ssh-info and scp --See [SSH into a job](http://docs.picloud.com/job_mgmt_adv.html#client-adv-ssh-into-job) and some [rough notes](https://www.evernote.com/shard/s1/sh/a9fab233-1857-4f01-8437-805be0e6fe22/593a1224dd150d6cf1cea6bb9886c22d).  The following code shows how to use `picloud ssh-info JID` to get the right ssh scp commands.
# 
# You can read off the job id for your PiCloud notebook server from the upper right corner of https://www.picloud.com/accounts/notebook/:
# 
# <img src="https://www.evernote.com/shard/s1/sh/646f953b-2c86-4b52-9deb-6dbe4f6ebc9e/26894da1003bf19d26cb0033f89097b4/res/a6f9765c-fa23-4521-9b02-3660134c9b80/PiCloud_%7C_Notebook-20130404-110444.jpg.jpg?resizeSmall&width=832">
# 

# <codecell>

import re

# put the job id of your notebook server after ssh-info

NOTEBOOK_SERVER_RUNNING = False
NOTEBOOK_SERVER_JID = 501

def to_picloud(nb_name):
    scp_to_command =  "scp -q -i {identity} -P {port} {nb_name} {username}@{address}:/home/picloud/notebook/".format(nb_name=nb_name, **ssh_info_output)
    return scp_to_command

if NOTEBOOK_SERVER_RUNNING:
    ssh_info_output = !picloud ssh-info $NOTEBOOK_SERVER_JID
    ssh_info_output = dict(zip( *[filter(None, re.split("\s+", l)) for l in ssh_info_output]))
#print ssh_info_output

    ssh_command = "ssh -q -i {identity} {username}@{address} -p {port}".format(**ssh_info_output)


    print ssh_command
    print to_picloud("Day_20_CommonCrawl.ipynb")

# you can even run the scp command from within iPython notebook -- uncomment following lines
#    to_picloud = to_picloud("Day_20_CommonCrawl.ipynb")
#    ! $to_picloud

# <markdowncell>

# **Running scp to the live notebook server machine will actually update the notebooks.**

# <headingcell level=1>

# Recasting this as picloudutil utility

# <markdowncell>

# I've packaged up a utility to move files using ssh and scp

# <codecell>

from wwod import picloud

# <codecell>

# pass in the job info for your running notebook server id -- if you have a notebook server running

import cloud
cloud.shortcuts.ssh.get_ssh_info(506)

# <codecell>

import cloud
cloud.shortcuts.ssh.get_ssh_command(506)

# <codecell>

# added scp
from wwod import picloud
picloud.to_picloud_cmd('me', 506)

