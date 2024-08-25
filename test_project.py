from project.project import url_checker, shorten, expand
import pytest


def test_url_checker():
    assert url_checker("https://www.google.com/") == "https://www.google.com/"
    with pytest.raises(SystemExit):
        assert url_checker("not a url")



def test_shorten():
    assert "tinyurl" in shorten("https://www.google.com/")
    with pytest.raises(SystemExit):
        assert shorten("https://tinyurl.com/badyx9h")


def test_expand():
    assert "google" in expand("https://tinyurl.com/badyx9h")

