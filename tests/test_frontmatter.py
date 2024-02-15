from pytest import fixture

from new_site.build import parse_yaml_frontmatter


@fixture
def no_frontmatter():
    return """
hello
"""


@fixture
def incorrect_frontmatter():
    return """
---
title: hello
--
hi
"""


@fixture
def mismatch_fences():
    return """
-------
title: hello
---

hi
"""


def test_no_frontmatter(no_frontmatter):
    frontmatter, content = parse_yaml_frontmatter(no_frontmatter[1:])
    assert frontmatter is None
    assert content.strip() == "hello"


def test_incorrect_frontmatter(incorrect_frontmatter):
    frontmatter, content = parse_yaml_frontmatter(incorrect_frontmatter[1:])
    assert frontmatter is None
    assert content.strip() == incorrect_frontmatter.strip()


def test_mismatch_fences(mismatch_fences):
    frontmatter, content = parse_yaml_frontmatter(mismatch_fences[1:])

    assert isinstance(frontmatter, dict)
    assert "title" in frontmatter
    assert frontmatter["title"] == "hello"
    assert content.strip() == "hi"
