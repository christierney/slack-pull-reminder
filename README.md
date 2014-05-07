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

You will need a personal token or room notification token:
https://www.hipchat.com/docs/apiv2/auth

### options

* `-r`, `--read` [required]: the name or id of the HipChat room to notify
* `-a`, `--auth` [required]: a HipChat v2 API auth token (personal or room)
* `-d`, `--domain`: the GitHub domain to query (defaults to `api.github.com`.)
  Do not include protocol or path components. Example: `github.mydomain.com`.
* '-c', '--color': the background color to use for the room notification.
  Choices are yellow, green, red, purple, gray, or random (defaults to yellow.)
* `repos` [required]: one or more repositories to check for open pull requests.
  These are positional arguments and must come after all other options.
  The syntax is `<user|org>/<repo>`, e.g. `github/hubot`.

### example

Report open pull requests from the `github/hubot` repo
to the HipChat room named `myroom`,
using HipChat auth token `abc123`.

    remind.py --room=myroom --auth=abc123 github/hubot

Report open pull requests from `myorg/a` and `myuser/b` repos
on a GitHub Enterprise server hosted at `github.mydomain.com`
to the HipChat room with ID `1234`,
using HipChat auth token `abc123`.

    remind.py -d github.mydomain.com -r 1234 -a abc123 myorg/a myuser/b

Suggestion: create a shell script that calls this with your desired arguments,
and run it regularly with `cron`.

## caveats

Requires python3. Blows up badly if any API requests fail for any reason.

## possible improvements

* consider reading token from a configuration file
* allow GitHub credentials for non-public repos or enterprise servers
* better error handling
