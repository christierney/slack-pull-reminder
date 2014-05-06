Script that checks a specified list of GitHub repositories
for open pull requests,
and sends a reminder to a specified HipChat room.

## why

We have a large number of developers working on a large number of repositories.
The quantity of notifications from GitHub is overwhelming
and most people ignore them.
There is no 'inbox' where you can find pull requests that need to be reviewed,
so devs who are waiting on reviews have to manually nag people.

## how

Create a personal token or room notification token:
https://www.hipchat.com/docs/apiv2/auth

Usage:

    remind.py --room=<room name> --auth=<token> repo1 [repo2 repo3... repoN]

Suggestion: run it regularly with `cron`.

## caveats

Requires python3. Blows up badly if any API requests fail for any reason.

## possible improvements

* consider reading token from a configuration file
* allow GitHub credentials for non-public repos or enterprise servers
* better error handling
