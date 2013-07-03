#!/usr/bin/env python

import argparse
import grequests
import requests
import logging
import sys

BASE_FB_URL = 'https://graph.facebook.com'

def chunks(l, n):
    '''Split l into n-sized chunks'''
    for i in range(0, len(l), n):
        yield l[i:i+n]

def parse_id(url):
    '''Recover the FB ID from the Notifications URL'''
    return url.split('/')[3]

def main():
    parser = argparse.ArgumentParser(description='Sends a Facebook notification to each of a list of FB users. See https://developers.facebook.com/docs/concepts/notifications/ for more information.')
    notifier_args = parser.add_argument_group('Notifier arguments')
    notifier_args.add_argument('-f', '--recipients-file', type=argparse.FileType('rt'), required=True, help='File containing list of recipients (newline-delimited FB IDs)')
    notifier_args.add_argument('-c', '--max-concurrent', default=10, type=int, help='Maximum number of concurrent requests (default: 10, max: 100)')
    notifier_args.add_argument('-l', '--log-level', default="warn", help='Log level (debug, info, [default] warn, error)')
    
    # Facebook parameters    
    fb_args = parser.add_argument_group('Facebook arguments')            
    fb_args.add_argument('-a', '--access-token', required=True, help='App access token')
    fb_args.add_argument('-t', '--template', required=True, help='Customized notification text')
    fb_args.add_argument('-r', '--ref', help='Tag for separating notifications into groups so they can be tracked independently')
    fb_args.add_argument('-u', '--href', help='Relative path/GET params of the target')

    args = parser.parse_args()

    log = logging.getLogger('fb_notifier')
    ch = logging.StreamHandler(sys.stdout)    
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s')    
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(getattr(logging, args.log_level.upper()))

    user_ids = args.recipients_file.read().splitlines()
    log.info("Found %s user IDs" % len(user_ids))

    session = requests.session()
    rs = [grequests.post("%s/%s/notifications" % (BASE_FB_URL, user_id), session=session, params={
            'access_token': args.access_token,
            'template': args.template,
            'ref': args.ref,
            'href': args.href
        }) for user_id in user_ids]

    requests_completed = 0
    chunk_size = args.max_concurrent if args.max_concurrent > 100 else 100
    for s in chunks(rs, chunk_size):
        responses = grequests.map(s, size=args.max_concurrent)        
        for r in responses:
            try:
                if r.status_code >= 300:
                    log.warn((r.status_code, parse_id(r.url), r.text))
                else:
                    log.debug((r.status_code, parse_id(r.url), r.text))
            finally:
                r.raw.release_conn()
        requests_completed += len(responses)
        log.info("Completed %s requests" % requests_completed)

if __name__ == "__main__":
    main()