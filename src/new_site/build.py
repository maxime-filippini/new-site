"""Functions used for building the site."""

import re
from typing import Any

import yaml

RE_FRONTMATTER = r"^(?:-{3,}\s*\n)((?:.*\n)*?)(?:-{3,}\s*\n)(.+)$"


def parse_yaml_frontmatter(text: str) -> tuple[Any | None, str]:
    """Parse the frontmatter for a blog post.

    Args:
        text (str): Contents of the markdown file.

    Returns:
        tuple[Any | None, str]: Frontmatter, content.
    """
    match = re.match(RE_FRONTMATTER, text)

    if not match:
        return None, text

    groups = match.groups()

    if not groups:
        return None, text

    return yaml.safe_load(match.groups()[0]), groups[1]
