#!/usr/bin/env python

import argparse
import grequests
import requests

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
    notifier_args.add_argument('-v', '--verbose', const=True, default=False, nargs='?', help='Show all results (instead of just failures)')
    notifier_args.add_argument('-q', '--quiet', const=True, default=False, nargs='?', help='Show no results')
    
    # Facebook parameters    
    fb_args = parser.add_argument_group('Facebook arguments')            
    fb_args.add_argument('-a', '--access-token', required=True, help='App access token')
    fb_args.add_argument('-t', '--template', required=True, help='Customized notification text')
    fb_args.add_argument('-r', '--ref', help='Tag for separating notifications into groups so they can be tracked independently')
    fb_args.add_argument('-u', '--href', help='Relative path/GET params of the target')

    args = parser.parse_args()

    user_ids = args.recipients_file.read().splitlines()

    session = requests.session()
    rs = [grequests.post("%s/%s/notifications" % (BASE_FB_URL, user_id), session=session, params={
            'access_token': args.access_token,
            'template': args.template,
            'ref': args.ref,
            'href': args.href
        }) for user_id in user_ids]

    chunk_size = args.max_concurrent if args.max_concurrent > 100 else 100
    for s in chunks(rs, chunk_size):
        responses = grequests.map(s, size=args.max_concurrent)
        for r in responses:
            try:
                if not args.quiet and (args.verbose or r.status_code >= 300): 
                    print (r.status_code, parse_id(r.url), r.text)
            finally:
                r.raw.release_conn()

if __name__ == "__main__":
    main()