#!/usr/bin/env python3

'''
This script gathers a list of open pull requests
from one or more GitHub repositories,
and reports them to a HipChat room.

The purpose is to gently remind people to deal with open requests,
e.g. by reviewing, merging, or closing them.

Usage:
    # report a single repo from github.com, using long param names:
    reminder.py --room <HipChat room> --auth <HipChat token> user/repo

    # report multiple repos:
    reminder.py --room <room> --auth <auth> user1/repo1 org/repo2 user2/repo3

    # report a single repo from a GitHub Enterprise domain,
    # using short param names:
    reminder.py -d <GitHub Enterprise domain> -r <room> -a <token> user/repo
'''

import argparse
import re
from urllib.request import urlopen, Request
import json

def remind(domain, room, auth, repos):
    '''Collect open pull requests from repos and post links to room.'''

    base = 'https://%s' % domain
    if domain != 'api.github.com':
        base += '/api/v3'

    urls = [url for repo in repos for url in _pulls(base, repo)]
    # note: \n\t won't render correctly in the linux client,
    # but it's fine in others
    msg = '\n\t'.join(urls)
    if msg:
        _post('@here please get these reviewed:\n\t' + msg, room, auth)

def _pulls(base, repo):
    '''Collect links to open pull requests from repo.'''

    data = urlopen('%s/repos/%s/pulls' % (base, repo)).read().decode('utf-8')
    return [p['html_url'] for p in json.loads(data)]

def _post(msg, room, auth):
    '''Post a message to a HipChat room.'''

    url = 'https://api.hipchat.com/v2/room/%s/notification' % room
    data = json.dumps({
        'message': msg,
        'message_format': 'text'
    }).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % auth
    }
    urlopen(Request(url, data, headers)).close()


_VALID_REPO = re.compile(r"[^/]+/[^/]+")
def _repo(arg):
    '''Check that an argument is a valid repo name (user/repo).'''

    if _VALID_REPO.fullmatch(arg):
        return arg
    else:
        raise argparse.ArgumentTypeError('%s is not a valid repo' % arg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Check for open pull requests.',
        epilog='''Example: reminder.py --room myroom
            --auth A0223lkasd098dfglkj235 github/hubot''')
    parser.add_argument(
        '-d', '--domain', default='api.github.com',
        help='your GitHub enterprise domain')
    parser.add_argument(
        '-r', '--room', required=True,
        help='the name or id of the room to notify')
    parser.add_argument(
        '-a', '--auth', required=True,
        help='a room notification or personal token from HipChat')
    parser.add_argument(
        'repos', nargs='+', type=_repo, metavar='repo',
        help='''one or more repositories to check for pull requests,
                specified as "<owner>/<repo>"''')
    opts = parser.parse_args()
    remind(opts.domain, opts.room, opts.auth, opts.repos)
