import argparse
import sys
import os
import re
import shutil
from pathlib import Path

from htmlsite.md import markdown_to_html_node


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "basepath",
        type=str,
        help="Base path to build the web",
    )
    parser.add_argument(
        "--build-directory",
        type=str,
        default="public",
        nargs="?",
        help="Directory where the web will be built on.",
    )
    args = parser.parse_args(sys.argv[1:])

    copy("static", args.build_directory)
    generate_pages_recursive(args.basepath, "content", args.build_directory)


def generate_pages_recursive(basepath: str, source: str, target: str) -> None:
    if not os.path.exists(source):
        raise TypeError("Source path must exists.")

    if os.path.isdir(source):
        for file in os.listdir(source):
            generate_pages_recursive(
                basepath, os.path.join(source, file), target=os.path.join(target, file)
            )
    else:
        target_path = Path(target).with_suffix(".html")
        generate_page(basepath, source, "template.html", target_path.as_posix())


def extract_title(md: str) -> str:
    return next(iter(re.findall(r"^# (.*)", md, re.MULTILINE)), "")


def generate_page(
    basepath: str, from_path: str, template_path: str, dest_path: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        from_content = file.read()

    with open(template_path) as file:
        template_content = file.read()

    dest_content = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    dest_content = (
        template_content.replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", dest_content)
    )
    dest_path: Path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(dest_content)


def copy(source: str, target: str) -> None:
    if not os.path.exists(source):
        raise TypeError("Source path must exists.")

    shutil.rmtree(target, ignore_errors=True)
    __copy(source, target)


def __copy(source: str, target: str):
    if os.path.isdir(source):
        os.makedirs(target, exist_ok=True)
        for file in os.listdir(source):
            __copy(os.path.join(source, file), target=os.path.join(target, file))
    else:
        shutil.copy(source, target)
