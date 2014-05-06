#!/usr/bin/env python3

import argparse
import re
from urllib.request import urlopen, Request
import json
from itertools import chain

class Reminder:
    def __init__(self, domain, room, auth, repos):
        self.base = 'https://%s' % domain
        if domain != 'api.github.com': self.base += '/api/v3'
        self.room = room
        self.auth = auth
        self.repos = repos

    def remind(self):
        urls = chain.from_iterable(map(self._pulls, self.repos))
        # note: \n won't render correctly in the linux client, but it's fine in others
        msg = '\n'.join(urls)
        if msg: self._post('@here please get these reviewed:\n' + msg)

    def _pulls(self, repo):
        data = urlopen(self.base + '/repos/%s/pulls' % repo).read().decode('utf-8')
        return [p['html_url'] for p in json.loads(data)]

    def _post(self, msg):
        url = 'https://api.hipchat.com/v2/room/%s/notification' % self.room
        data = json.dumps({'message': msg, 'message_format': 'text'}).encode('utf-8')
        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer %s' % self.auth
                }
        urlopen(Request(url, data, headers)).close()


valid_repo = re.compile(r"[^/]+/[^/]+")
def repo(s):
    if valid_repo.fullmatch(s): return s
    else: raise argparse.ArgumentTypeError('%s is not a valid repo' % s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for open pull requests.',
            epilog='''Example:

reminder.py --room myroom --auth A0223lkasd098dfglkj235 github/hubot''')
    parser.add_argument('-d', '--domain', default='api.github.com',
            help='your GitHub enterprise domain')
    parser.add_argument('-r', '--room', required=True,
            help='the name or id of the room to notify')
    parser.add_argument('-a', '--auth', required=True,
            help='a room notification or personal token from HipChat')
    parser.add_argument('repos', nargs='+', type=repo, metavar='repo',
            help='one or more repositories to check for pull requests, specified as "<owner>/<repo>"')

    Reminder(**vars(parser.parse_args())).remind()
