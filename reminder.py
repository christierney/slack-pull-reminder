#!/usr/bin/env python3

'''
This script gathers a list of open pull requests
from one or more GitHub repositories,
and reports them to a Slack channel.

The purpose is to gently remind people to deal with open requests,
e.g. by reviewing, merging, or closing them.

Usage:
    # report a single repo from github.com, using long param names:
    reminder.py --hook <webhook url> user/repo

    # report multiple repos:
    reminder.py --hook <webhook url> user1/repo1 org/repo2 user2/repo3

    # report a single repo from a GitHub Enterprise domain,
    # using short param names:
    reminder.py -d <GitHub Enterprise domain> -k <hook> user/repo
'''

import argparse
import re
from urllib.request import urlopen, Request
import base64
import json

def remind(domain, hook, user, pw, repos, color):
    '''Collect open pull requests from repos and post links to channel.'''

    base = 'https://%s' % domain
    if domain != 'api.github.com':
        base += '/api/v3'

    urls = [url for repo in repos for url in _pulls(base, repo, user, pw)]
    if urls:
        _post(urls, hook, color)

def _pulls(base, repo, user, pw):
    '''Collect links to open pull requests from repo.'''

    url = '%s/repos/%s/pulls' % (base, repo)
    headers = {}
    if pw is not None:
        raw = "%s:%s" % (user, pw)
        auth = "Basic " + base64.b64encode(raw.encode()).decode("ascii")
        headers = {
            'Authorization': auth
        }

    data = urlopen(Request(url, headers=headers)).read().decode('utf-8')
    return [p['html_url'] for p in json.loads(data)]

def _post(urls, hook, color):
    '''Post a message to a Slack channel.'''

    msg = 'Please complete %d review' % len(urls)
    if (len(urls) > 1): msg += 's'

    if (color == 'dynamic'): color = _choose_color(len(urls))

    data = json.dumps({
        'attachments': [{
            'fallback': msg.replace('complete', 'COMLETE'),
            'pretext': msg,
            'text' : '\n'.join(urls),
            'color': color
        }]
    }).encode('utf-8')
    headers = {
        'Content-Type': 'application/json'
    }
    urlopen(Request(hook, data, headers)).close()

def _choose_color(n):
    if (n < 3): return 'good'
    elif (n < 5): return 'warning'
    elif (n < 10): return 'danger'
    else: return '#000000'

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
        '-k', '--hook', required=True,
        help='the webhook URL from the slack app installation')
    parser.add_argument(
        '-u', '--user', required=False,
        help='a GitHub username to pair with the password arg')
    parser.add_argument(
        '-p', '--password', required=False,
        help='a password or personal access token from GitHub (for accessing private repos)')
    parser.add_argument(
        '-c', '--color', default='dynamic',
        help='the sidebar color to use for the notification')
    parser.add_argument(
        'repos', nargs='+', type=_repo, metavar='repo',
        help='''one or more repositories to check for pull requests,
                specified as "<owner>/<repo>"''')
    opts = parser.parse_args()
    remind(opts.domain, opts.hook, opts.user, opts.password, opts.repos, opts.color)
