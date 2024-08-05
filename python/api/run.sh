#!/bin/sh
# count="0"
# for count in 1 2 3 4 5; do
#     python manage.py db upgrade
#     if [[ "$?" == "0" ]]; then
#         break
#     fi
#     echo Upgrade command failed, retrying in 5 secs...
#     sleep 5
#     count=$[$count+1]
# done


if [[ `hostname` == *prashants-MacBook-Pro.local* ]]; then
    # gunicorn -k gevent -w 5 --reload -b 0.0.0.0:5000 run:app
    gunicorn --reload -b 0.0.0.0:5000 run:app
else
    gunicorn -k gevent -w 5 -b 0.0.0.0:$PORT run:app
    # gunicorn --reload -b 0.0.0.0:$PORT run:app
fi
