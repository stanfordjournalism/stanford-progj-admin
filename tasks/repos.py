import os
import re
import sys

import github
from invoke import task


@task(
help={
    'suffix': 'Append suffix to REPO_SEARCH_FILTER when filtering repo list.',
    'custom-filter': 'Substitute custom filter for default REPO_SEARCH_FILTER.'
})
def search(c, suffix='', custom_filter=''):
    """
    Search for repos related to this course.

    By default, filters list of repos by name based
    on REPO_SEARCH_FILTER environment variable.
    """
    if not custom_filter:
        try:
            keyword = os.environ['REPO_SEARCH_FILTER']
        except KeyError:
            msg = ('\n\tYou must use --custom-filter or '
                   'set the REPO_SEARCH_FILTER '
                   'environment variable in .env file.\n')
            sys.exit(msg)
    if custom_filter:
        keyword = custom_filter
    elif suffix:
        keyword += suffix
    query = "{} in:name".format(keyword)
    api_key = os.environ['GITHUB_API_KEY']
    g = github.Github(api_key)
    repos = g.search_repositories(query)
    for repo in repos:
        # HACK: Further filter results from search API,
        # which is keyword-based and doesn't precisely
        # match on repo names (e.g. comm-177p-assignment-3
        # is returned when searching for comm-177p-assignment-1)
        if keyword in repo.ssh_url:
            print(repo.ssh_url)

@task(help={
    'repos-file': 'Path to text file containing ssh URLs to clone'
})
def clone(c, repos_file):
    """Clone one or more GitHub repos locally
    from a file containing a list of ssh-based repo URLs.

    The repos file should have one ssh url per row.
    It can be produced easily using the repos.search task:

        $ invoke repos.search > repo_list.txt

    """
    pattern = r'git@github.com:(.+)/(.+).git'
    with open(repos_file,'r') as fh:
        for url in fh:
            clean_url = url.strip()
            user, project = re.match(pattern, clean_url).groups()
            project_dir = 'cloned_repos/{}'.format(project)
            clone_dir = os.path.join(project_dir, user)
            c.run('mkdir -p {}'.format(project_dir))
            if os.path.exists(clone_dir):
                print('Skipping already cloned repo: {}'.format(clone_dir))
            else:
                c.run('git clone {} {}'.format(clean_url, clone_dir))
