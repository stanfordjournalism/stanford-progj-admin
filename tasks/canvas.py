import csv
import os
import json
import pytz
import re
import sys
import urllib.parse

from canvasapi import Canvas
from invoke import task


@task()
def roster(c):
    """show student roster"""
    course = get_canvas_course()
    for enrollee in course.get_enrollments():
        if enrollee.role == 'StudentEnrollment':
            print("{} ({})".format(
                enrollee.user['sortable_name'],
                enrollee.user['login_id']
            ))

@task()
def assignments(c, need_grading=False):
    """Display assignment metadata"""
    course = get_canvas_course()
    assignments = []
    print("Fetching assignments data from Canvas...")
    for assignment in course.get_assignments():
        name = assignment.name
        atype, number, title = parse_assignment_name(name)
        due = assignment.due_at
        need_grading = assignment.needs_grading_count
        assignments.append({
            'type': atype,
            'number': number,
            'title': title,
            'due': due,
            'need_grading': need_grading,
            'url': assignment.html_url
        })
    print("Generating data/assignments.csv")
    os.makedirs('data/', exist_ok=True)
    with open('data/assignments.csv', 'w') as fh:
        header = [
            'type',
            'number',
            'title',
            'need_grading',
            'due',
            'url'
        ]
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()
        writer.writerows(assignments)


@task()
def assignment_repos(c):
    """Generate CSVs containing GitHub URLs for code assignments"""
    course = get_canvas_course()
    code_assignments = {}
    print("Compiling code assignment submissions from Canvas...")
    urls = {}
    for assignment in course.get_assignments():
        # Only process submissions of online URLs (which should
        # point to GitHub projects)
        if 'online_url' in assignment.submission_types:
            atype, number, title = parse_assignment_name(assignment.name)
            for submission in assignment.get_submissions():
                # Skip if not submitted
                if submission.workflow_state == 'unsubmitted':
                    continue
                # Only process GitHub urls to allow for possibility
                # of GDoc written assignments
                # NOTE: We save url in a one-element list for
                # downstream "writerows"
                if 'github.com' in submission.url:
                    clean_url = standardize_repo_url(submission.url)
                    urls.setdefault(
                        (atype, str(number)), []
                    ).append([clean_url])
    print("Generating repo lists...")
    os.makedirs('data/', exist_ok=True)
    for key, urls in urls.items():
        atype, number = key
        outfile = create_repo_urls_file(atype, number, urls)
        print(' - {}'.format(outfile))


### Helpers ###

def get_canvas_course():
    url, api_key, course_id = canvas_configs()
    canvas = Canvas(url, api_key)
    return canvas.get_course(course_id)


def canvas_configs():
    vars = [
        'CANVAS_BASE_URL',
        'CANVAS_API_KEY',
        'CANVAS_COURSE_ID'
    ]
    env_vars = []
    for var in vars:
        try:
            env_vars.append(os.environ[var])
        except KeyError:
            msg = '\n{} environment variable must be set!\n'.format(var)
            sys.exit(msg)
    return env_vars


def parse_assignment_name(name):
    atype, number, title = re.match(
        r'(.+)(\d+)(.+)',
        name
    ).groups()
    return [
        atype.replace('-', '').strip().lower(),
        int(number.strip()),
        title.strip().lstrip('-').strip()
    ]


def standardize_repo_url(url):
    """
    Clean up case where students submit link to file
    inside repo rather than base repo URL.
    """
    parsed = urllib.parse.urlparse(url)
    path_bits = parsed.path.split('/')
    user = path_bits[1]
    repo = path_bits[2]
    return "https://github.com/{}/{}".format(user, repo)


def create_repo_urls_file(atype, number, urls):
    outfile = 'data/repos_{}_{}.csv'.format(atype, number)
    with open(outfile, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerows(urls)
    return outfile

