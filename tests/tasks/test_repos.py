import pytest
from tasks.repos import convert_https_to_ssh, extract_data_from_url


@pytest.mark.parametrize("test_url,expected",[
    (
    "https://github.com/user/some-repo/",
    "git@github.com:user/some-repo.git"
    ),
    (
    "https://github.com/user/some-repo",
    "git@github.com:user/some-repo.git"
    )
])
def test_convert_https_urls(test_url, expected):
    assert convert_https_to_ssh(test_url) == expected


def test_extract_data_from_urls():
    url = "https://github.com/user/some-repo/"
    expected = ('user', 'some-repo')
    assert extract_data_from_url(url) == expected
