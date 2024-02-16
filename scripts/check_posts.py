import argparse
import pathlib
from typing import Sequence

from new_site.build import parse_yaml_frontmatter
from new_site.schemas import BlogPostMetadata


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args(argv)
    path_dir = pathlib.Path(args.dir)

    for path_file in path_dir.rglob("*.md"):
        print(path_file)

        with open(path_file, "r") as fd:
            data = fd.read()

        frontmatter, _ = parse_yaml_frontmatter(data)
        if not frontmatter:
            raise ValueError("hello")
        print(BlogPostMetadata(**frontmatter))


if __name__ == "__main__":
    raise SystemExit(main())
