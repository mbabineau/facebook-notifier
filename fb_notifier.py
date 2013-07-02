#!/usr/bin/env python

import argparse
import grequests

BASE_FB_URL = 'https://graph.facebook.com'

def main():
    parser = argparse.ArgumentParser(description='Sends a Facebook notification to each of a list of FB users. See https://developers.facebook.com/docs/concepts/notifications/ for more information.')
    notifier_args = parser.add_argument_group('Notifier arguments')
    notifier_args.add_argument('-f', '--recipients-file', type=argparse.FileType('rt'), required=True, help='File containing list of recipients (newline-delimited FB IDs)')
    notifier_args.add_argument('-c', '--max-concurrent', default=10, help='Maximum number of concurrent requests')
    
    # Facebook parameters    
    fb_args = parser.add_argument_group('Facebook arguments')            
    fb_args.add_argument('-a', '--access-token', required=True, help='App access token')
    fb_args.add_argument('-t', '--template', required=True, help='Customized notification text')
    fb_args.add_argument('-r', '--ref', help='Tag for separating notifications into groups so they can be tracked independently')
    fb_args.add_argument('-u', '--href', help='Relative path/GET params of the target')

    args = parser.parse_args()

    user_ids = args.recipients_file.read().splitlines()

    rs = (grequests.post("%s/%s/notifications" % (BASE_FB_URL, user_id), params={
            'access_token': args.access_token,
            'template': args.template,
            'ref': args.ref,
            'href': args.href
        }) for user_id in user_ids)

    print grequests.map(rs, size=args.max_concurrent)

if __name__ == "__main__":
    main()