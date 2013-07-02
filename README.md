facebook-notifier
=================

Simple tool to send a Facebook Notifications to each of a list of Facebook users via the [Notifications API](https://developers.facebook.com/docs/concepts/notifications/). Configurable concurrency.

Example:
```
fb_notifier.py -f user_ids.txt -a '123456789000|abc123abc123_abc123' -t 'This is a message from your friendly application'
[<Response [200]>, <Response [200]>, <Response [200]>]
```

Requirements
------------

 * [grequests](https://github.com/kennethreitz/grequests)
 * Facebook `app access token` ([FB documentation](https://developers.facebook.com/docs/opengraph/howtos/publishing-with-app-token/))

Usage
------------

```
usage: fb_notifier.py [-h] -f RECIPIENTS_FILE [-c MAX_CONCURRENT] -a
                      ACCESS_TOKEN -t TEMPLATE [-r REF] [-u HREF]

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
                        Maximum number of concurrent requests

Facebook arguments:
  -a ACCESS_TOKEN, --access-token ACCESS_TOKEN
                        App access token
  -t TEMPLATE, --template TEMPLATE
                        Customized notification text
  -r REF, --ref REF     Tag for separating notifications into groups so they
                        can be tracked independently
  -u HREF, --href HREF  Relative path/GET params of the target
```

