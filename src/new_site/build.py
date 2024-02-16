"""Functions used for building the site."""

import os
import pathlib
import re
import shutil
from typing import Any

import jinja2
import markdown
import yaml
from pydantic import BaseModel

from new_site.schemas import BlogPostMetadata

RE_FRONTMATTER = r"^(-{3,}\s*\n)((?:.*\n)*?)(-{3,}\s*\n)"


class NoFrontMatterFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("No frontmatter found in the file!")


def parse_yaml_frontmatter(text: str) -> tuple[Any, str]:
    """Parse the frontmatter for a blog post.

    Args:
        text (str): Contents of the markdown file.

    Returns:
        tuple[Any | None, str]: Frontmatter, content.
    """
    match = re.match(RE_FRONTMATTER, text)

    if not match:
        raise NoFrontMatterFoundError

    groups = match.groups()

    if not groups:
        raise NoFrontMatterFoundError

    fence_start, frontmatter, fence_end = match.groups()
    n_chars = len(frontmatter) + len(fence_start) + len(fence_end)

    return yaml.safe_load(frontmatter), text[n_chars:]


class MarkdownExtension(BaseModel):
    pass


class ArithmatexExtension(MarkdownExtension):
    __name__ = "pymdownx.arithmatex"

    generic: bool


class WebsiteBuilder:
    def __init__(
        self,
        source_dir: os.PathLike[str],
        build_dir: os.PathLike[str],
        template_dir: os.PathLike[str],
    ) -> None:
        self._source_dir = pathlib.Path(source_dir)
        self._build_dir = pathlib.Path(build_dir)
        self._template_dir = pathlib.Path(template_dir)
        self._markdown_extensions: list[MarkdownExtension] = []
        self._update_markdown_spec()
        self._init_jinja2_env()

    def _init_jinja2_env(self) -> None:
        self._jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self._template_dir)
        )

    def _init_build_dir(self) -> None:
        if not self._build_dir.exists():
            self._build_dir.mkdir()
        else:
            shutil.rmtree(self._build_dir)

    def _update_markdown_spec(self) -> None:
        self._md = markdown.Markdown(
            extensions=[ext.__name__ for ext in self._markdown_extensions],
            extension_configs={
                ext.__name__: ext.model_dump() for ext in self._markdown_extensions
            },
        )

    def add_markdown_extension(self, extension: MarkdownExtension) -> None:
        self._markdown_extensions.append(extension)
        self._update_markdown_spec()

    def _collect_frontmatters(self) -> list[BlogPostMetadata]:
        out = []
        for path_file in self._source_dir.rglob("*.md"):
            with open(path_file, "r") as fd:
                text = fd.read()

            frontmatter, _ = parse_yaml_frontmatter(text)
            out.append(BlogPostMetadata(**frontmatter))

        return out

    def _convert_single_file(
        self, path: os.PathLike[str]
    ) -> tuple[BlogPostMetadata, str]:
        with open(path, "r") as fd:
            text = fd.read()

        frontmatter, content = parse_yaml_frontmatter(text)
        return BlogPostMetadata(**frontmatter), self._md.convert(content)

    def build_site(self) -> None:
        self._init_build_dir()
        self._copy_static_files()
        self._copy_markdown_files()

    def _copy_static_files(self) -> None:
        static_src = self._source_dir / "static"

        if static_src.exists():
            shutil.copytree(static_src, self._build_dir / "static")

    def _copy_markdown_files(self) -> None:
        pass


class MarkdownParser:
    def __init__(self) -> None:
        pass
