import os

import github
from invoke import task


@task()
def list(c):
    "Show GitHub invitations"
    api_key = os.environ['GITHUB_API_KEY']
    # api_key = 'bla'
    g = github.Github(api_key)
  
    me = g.get_user()
    invites_list = me.get_invitations()
    for repo_invite in invites_list:
        # print(repo_invite)
        me.accept_invitation(repo_invite)
        print(repo_invite, ' has been accepted.')


    # TODO: list invites
    # https://developer.github.com/v3/repos/invitations/
    # https://developer.github.com/v3/repos/invitations/#list-a-users-repository-invitations
    # https://pygithub.readthedocs.io/en/latest/github_objects/Invitation.html

@task()
def accept(c):
    "Accept one or more GitHub invites"
    api_key = os.environ['GITHUB_API_KEY']
    # api_key = 'bla'
    g = github.Github(api_key)

    # TODO: accept invites
    # https://pygithub.readthedocs.io/en/latest/github_objects/Invitation.html
    # https://developer.github.com/v3/repos/invitations/
    # https://developer.github.com/v3/repos/invitations/#accept-a-repository-invitation
