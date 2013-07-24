facebook-notifier
=================

Simple tool to send a Facebook Notifications to each of a list of Facebook users via the [Notifications API](https://developers.facebook.com/docs/concepts/notifications/). Configurable concurrency.

Example:
```
$ fb_notifier.py -f user_ids.txt -a '123456789000|abc123abc123_abc123' -t 'This is a message from your friendly application' -l DEBUG
2013-07-24 11:24:46,642 [fb_notifier] INFO - Found 3 user IDs
2013-07-24 11:24:47,036 [fb_notifier] DEBUG - (200, u'100012345678', u'{"success":true}')
2013-07-24 11:24:47,036 [fb_notifier] DEBUG - (200, u'100087654321', u'{"success":true}')
2013-07-24 11:24:47,036 [fb_notifier] WARNING - (404, u'fake_user_abc123', u'{"error":{"message":"(#803) Some of the aliases you requested do not exist: fake_user_abc123","type":"OAuthException","code":803}}')
2013-07-24 11:22:47,036 [fb_notifier] INFO - Completed 3 requests
```

Requirements
------------

 * [grequests](https://github.com/kennethreitz/grequests)
 * [requests](https://github.com/kennethreitz/requests)
 * [argparse](https://pypi.python.org/pypi/argparse) (if below Python 2.7 or 3.2)
 * Facebook `app access token` ([FB documentation](https://developers.facebook.com/docs/opengraph/howtos/publishing-with-app-token/))

Usage
------------

```
usage: fb_notifier.py [-h] -f RECIPIENTS_FILE [-c MAX_CONCURRENT]
                      [-l LOG_LEVEL] -a ACCESS_TOKEN -t TEMPLATE [-r REF]
                      [-u HREF]

Sends a Facebook notification to each of a list of FB users. See
https://developers.facebook.com/docs/concepts/notifications/ for more
information.

optional arguments:
  -h, --help            show this help message and exit

Notifier arguments:
  -f RECIPIENTS_FILE, --recipients-file RECIPIENTS_FILE
                        File containing list of recipients (newline-delimited
                        FB IDs)
  -c MAX_CONCURRENT, --max-concurrent MAX_CONCURRENT
                        Maximum number of concurrent requests (default: 10,
                        max: 100)
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Log level (debug, info, [default] warn, error)

Facebook arguments:
  -a ACCESS_TOKEN, --access-token ACCESS_TOKEN
                        App access token
  -t TEMPLATE, --template TEMPLATE
                        Customized notification text
  -r REF, --ref REF     Tag for separating notifications into groups so they
                        can be tracked independently
  -u HREF, --href HREF  Relative path/GET params of the target
```

