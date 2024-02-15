"""Functions used for building the site."""

import re
from typing import Any

import yaml

RE_FRONTMATTER = r"^(?:---\s*\n)((?:.*\n)*?)(?:---\s*\n)"


def parse_yaml_frontmatter(text: str) -> Any | None:
    """Parse the frontmatter for a blog post.

    Args:
        text (str): Contents of the markdown file.

    Returns:
        dict[str, Any] | None: Metadata or None if no frontmatter was provided.
    """
    match = re.match(RE_FRONTMATTER, text)

    if not match:
        return None

    groups = match.groups()

    if not groups:
        return None

    return yaml.safe_load(match.groups()[0])
