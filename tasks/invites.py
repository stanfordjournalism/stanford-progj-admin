import os

import github
from invoke import task


@task()
def list(c):
    "Show GitHub invitations"
    api_key = os.environ['GITHUB_API_KEY']
    g = github.Github(api_key)
    me = g.get_user()
    invites_list = me.get_invitations()
    for repo_invite in invites_list:
        print(repo_invite.html_url)

@task()
def accept(c):
    "Accept one or more GitHub invites"
    api_key = os.environ['GITHUB_API_KEY']
    g = github.Github(api_key)
    me = g.get_user()
    invites_list = me.get_invitations()
    for repo_invite in invites_list:
        me.accept_invitation(repo_invite)
        print(repo_invite.html_url, ' has been accepted.')
