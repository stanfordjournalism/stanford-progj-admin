import pytest
from tasks.canvas import standardize_repo_url


@pytest.mark.parametrize("test_url,expected",[
    (
    "https://github.com/user/some-repo/blob/master/some_file.py",
    "https://github.com/user/some-repo"
    ),
    (
    "https://github.com/user/some-repo/",
    "https://github.com/user/some-repo"
    )
])
def test_standardize_github_urls(test_url, expected):
    assert standardize_repo_url(test_url) == expected
