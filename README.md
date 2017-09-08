Script that checks a specified list of GitHub repositories
for open pull requests,
and sends a reminder to a specified Slack room.

## why

We have a large number of developers working on a large number of repositories.
The quantity of notifications from GitHub is overwhelming
and most people ignore them.
There is no 'inbox' where you can find pull requests that need to be reviewed,
so devs who are waiting on reviews have to manually nag people.

## how

You will need to create a Slack App and get a webhook URL for it.

If you want to access a private repo, you will also need a personal access
token: https://github.com/settings/tokens This token should have sufficient
scope to read repo information.

### options

* `-k`, `--hook` [required]: the webhook URL from the Slack App installation
* `-u`, `--user`: a GitHub username (required if accessing a private repo)
* `-p`, `--password`: a GitHub personal access token (required if accessing a
  private repo)
* `-d`, `--domain`: the GitHub domain to query (defaults to `api.github.com`.)
  Do not include protocol or path components. Example: `github.mydomain.com`.
* `-c`, `--color`: the sidebar color to use for the room notification.
* `repos` [required]: one or more repositories to check for open pull requests.
  These are positional arguments and must come after all other options.
  The syntax is `<user|org>/<repo>`, e.g. `github/hubot`.

### example

Report open pull requests from the `github/hubot` repo.

    remind.py --room=myroom --hook=<slack webhook url> github/hubot

Report open pull requests from `myorg/a` and `myuser/b` repos
on a GitHub Enterprise server hosted at `github.mydomain.com`.

    remind.py -d github.mydomain.com -k <slack webhook url> myorg/a myuser/b

Suggestion: create a shell script that calls this with your desired arguments,
and run it regularly with `cron`.

## caveats

Requires python3. Blows up badly if any API requests fail for any reason.

## possible improvements

* consider reading token from a configuration file
* allow GitHub credentials for non-public repos or enterprise servers
* better error handling
