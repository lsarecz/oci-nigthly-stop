# oci-nigthly-stop

Stops the OCI resources at night.
Also, change the licensing model of Autonomous Database to BYOL.


## Instances to be stopped

- Compute instance
- Autonomous Database
- Database (DBaaS)


## Prerequisites
- oci python SDK
- Python 3
- ocicli profile created and `oci setup config` executed


## How to use

1. Clone this repository

2. Open the file stop.py # Specify your config file where "according to the environment" is written.

3. Stop process is executed with the following command
    `python3 stop.py`
    
4. Logs are written to the standard output and error output. If necessary, redirect them to a log file.

5. Python scheduler is not used. If necessary, execute it periodically using cron.

    (The following is an example for executing every day at 24:00)
    `0 0 * * * cd /home/opc; python3 -u /home/opc/oci-nightly-stop/stop.py > /home/opc/log/stop_`date +\%Y\%m\%d-\%H\%M\%S`.log 2>&1`


## If you want to exclude an instance from being stopped

For each instance by setting whitelisted tag to 'Yes', you can exclude it from being stopped.

    - Tag Namespace: Monitoring
    - Tag Key：whitelisted
    - Value: yes
    
For a guide on how to set up tags: https://github.com/lsarecz/oci-nigthly-stop/blob/master/guide/howtoaddtags.md
