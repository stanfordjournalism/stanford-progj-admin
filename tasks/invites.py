import os

import github
from invoke import task


def decline_invitation(user, invitation):
    """Decline invite

    This feature doesn't appear to be built into PyGitHub.
    Using a quick-and-dirty hack of AuthenticatedUser.accept_invitation

    https://github.com/PyGithub/PyGithub/blob/4f00cbf2c449fba07dda76fd1a248f8023b00de1/github/AuthenticatedUser.py#L1253
    """
    assert isinstance(invitation, github.Invitation.Invitation) or isinstance(
        invitation, int
    )

    if isinstance(invitation, github.Invitation.Invitation):
        invite_id = invitation.id
    headers, data = user._requester.requestJsonAndCheck(
        "DELETE", f"/user/repository_invitations/{invite_id}", input={}
    )


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
def accept(c, interactive=False):
    "Accept one or more GitHub invites"
    api_key = os.environ['GITHUB_API_KEY']
    g = github.Github(api_key)
    me = g.get_user()
    invites_list = me.get_invitations()
    if interactive:
        print((
            "For each invite, chooose the letter for one of the below options:\n"
            "\tA - Accept\n"
            "\tD - Decline\n"
            "\tI - Ignore\n"
            "\nThe default is Accept (A). Lower-case choices will work fine.\n\n"
        ))
    for repo_invite in invites_list:
        if interactive:
            choice = input(f"{repo_invite.html_url} [A]: ").strip().lower()
            if choice not in ('d','i'):
                me.accept_invitation(repo_invite)
                print(f'Accepted {repo_invite.html_url}')
            if choice == 'd':
                decline_invitation(me, repo_invite)
                print(f'Decline {repo_invite.html_url}')
            if choice == 'i':
                print(f'Ignored {repo_invite.html_url}')


