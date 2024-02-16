import pathlib

from new_site.build import ArithmatexExtension
from new_site.build import WebsiteBuilder

ROOT_PATH = pathlib.Path(__file__).parent.parent


def _init_builder() -> WebsiteBuilder:
    builder = WebsiteBuilder(
        source_dir=ROOT_PATH / "site" / "src",
        build_dir=ROOT_PATH / "site" / "build",
        template_dir=ROOT_PATH / "src" / "new_site" / "templates",
    )

    builder.add_markdown_extension(ArithmatexExtension(generic=True))
    return builder


def main() -> int:
    builder = _init_builder()
    builder.build_site()
    # _copy_css
    # _copy_javascript

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
