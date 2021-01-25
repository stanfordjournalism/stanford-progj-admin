import os
import re
import sys
import urllib.parse

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
        if keyword in repo.html_url:
            print(repo.html_url)

@task(help={
    'repos-file': 'Path to text file containing https URLs to clone'
})
def clone(c, repos_file):
    """Clone one or more GitHub repos locally
    from a file containing a list of ssh-based repo URLs.

    The repos file should have one https url per row.
    This task converts HTTPS to SSH urls and clones the repo.
    The HTTPS urls file can be produced using

        $ invoke canvas.assigment-repos

        # or

        $ invoke repos.search > repo_list.txt

    """
    with open(repos_file,'r') as fh:
        for url in fh:
            clean_url = url.strip()
            user, repo_name = extract_data_from_url(clean_url)
            if 'repos_' in repos_file:
                assignment_type, number = re.match(
                    r'.*?repos_(.+?)_(\d+).csv',
                    repos_file
                ).groups()
                project_dir = 'cloned_repos/{}_{}'.format(assignment_type, number)
            else:
                project_dir = 'cloned_repos/{}'.format(repo_name)
            clone_dir = os.path.join(project_dir, user)
            os.makedirs(project_dir, exist_ok=True)
            if os.path.exists(clone_dir):
                print('Skipping already cloned repo: {}'.format(clone_dir))
            else:
                if 'gist' in clean_url:
                    ssh_url = convert_gist_to_ssh(clean_url)
                else:
                    ssh_url = convert_https_to_ssh(clean_url)
                c.run('git clone {} {}'.format(ssh_url, clone_dir))


def extract_data_from_url(url):
    bits = urllib.parse.urlparse(url).path.split('/')
    user = bits[1]
    repo = bits[2]
    return (user, repo)

def convert_https_to_ssh(url):
    user, repo = extract_data_from_url(url)
    return "git@github.com:{}/{}.git".format(user, repo)

def convert_gist_to_ssh(url):
    # Hash in URL indicates deep link which must be removed
    if '#' in url:
        url = re.sub('#.+', '', url)
    sha = url.split('/')[-1]
    return "git@gist.github.com:{}.git".format(sha)
