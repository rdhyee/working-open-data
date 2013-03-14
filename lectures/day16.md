% Day 16:  PiCloud / AWS / CommonCrawl
% Raymond Yee 
% March 14, 2013 (<http://bit.ly/wwod1316>)

# Agenda

* Getting set up on PiCloud


# PiCloud setup

* Sign up at <http://www.picloud.com/>, specifically <https://www.picloud.com/accounts/register/?>.  Although I used Google
authentication, I also went to <https://www.picloud.com/accounts/settings/> to set a regular password, which will be
necessary (?) for using Notebooks.

* You probably won't need to put in your credit card number.  If you stay on "trial membership" status, you get
20 hours/month free of C1 compute time ($1/month credit)

# Finding my custom environment

* Click on <https://www.picloud.com/accounts/environment/> and select "Public Environments" tab (the rightmost)
* Search for "Working" in "Explore Public Environments" search box to bring up the `/rdhyee/Working_with_Open_Data`
environment.  *Favorite* it so you can then use it with your own notebooks.

# PiCloud notebooks

Now go to <https://www.picloud.com/accounts/notebook/>.  Try out the `Primer` notebook while selecting the
`/rdhyee/Working_with_Open_Data` environment.

# Getting picloud set up on your local machine

To get the `cloud` Python library set up on your local machine and if you are running EPD, which has an out-of-date
`cloud` library, run
    
    pip install --upgrade cloud
    
and

    picloud setup

# how to ssh into your notebook machine

Once you have your local picloud setup going, you can [ssh into the job](http://docs.picloud.com/job_mgmt_adv.html#client-adv-ssh-into-job)

    picloud ssh notebook-job-id
    
Look at <https://www.picloud.com/accounts/jobs/> to find out the notebook-job-id

NB:  I don't know whether this functionality works on Windows though....


