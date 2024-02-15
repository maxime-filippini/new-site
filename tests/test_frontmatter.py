from pytest import fixture

from new_site.build import parse_yaml_frontmatter


@fixture
def test_file():
    with open("tests/fixtures/frontmatter.md", "r") as fd:
        return fd.read()


def test_parsing(test_file):
    parse_yaml_frontmatter(test_file)
