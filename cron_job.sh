#!/bin/bash
cd   /bbsparse/
echo "`date` running cron job"
## m h  dom mon dow   command
#0  */3  * * *   bash /bbsparse/cron_job.sh

python manage.py harvestlinks -c 30 > /data/bbsparse/logs/harvest.log 2>&1
