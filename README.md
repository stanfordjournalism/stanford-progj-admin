# stanford-progj-admin

Command-line utilities (using
[invoke](https://docs.pyinvoke.org/en/stable/)) to help
administer Stanford's Programming in Journalism course.

## Setup

```
git clone git@github.com:stanfordjournalism/stanford-progj-admin.git
cd stanford-progj-admin
pipenv install
```

Generate a [personal GitHub API token](https://github.com/settings/tokens).

Add your API token and GitHub username to a project `.env` file:

```
# Fill in your own info for below variables
echo GITHUB_USER=your_username >> .env
echo GITHUB_API_TOKEN=your_api_token >> .env
```

## Usage

```
# Activate env
cd stanford-progj-admin
pipenv shell

# See available commands
invoke --list
```
