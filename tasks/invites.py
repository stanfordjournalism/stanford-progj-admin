import os

import github
from invoke import task


@task()
def list(c):
    "Show GitHub invitations"
    api_key = os.environ['GITHUB_API_KEY']
    g = github.Github(api_key)
    # TODO: list invites
    # https://developer.github.com/v3/repos/invitations/
    # https://developer.github.com/v3/repos/invitations/#list-a-users-repository-invitations
    # https://pygithub.readthedocs.io/en/latest/github_objects/Invitation.html

@task()
def accept(c):
    "Accept one or more GitHub invites"
    api_key = os.environ['GITHUB_API_KEY']
    g = github.Github(api_key)
    # TODO: accept invites
    # https://pygithub.readthedocs.io/en/latest/github_objects/Invitation.html
    # https://developer.github.com/v3/repos/invitations/
    # https://developer.github.com/v3/repos/invitations/#accept-a-repository-invitation
