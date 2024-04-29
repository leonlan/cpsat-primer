"""
This file is used to build the `README.md` file from all markdown files in the current directory.
It also converts the markdown files to a format that can be used by the `mdbook` tool, which we
use to generate the website.
"""

import os
import re
from pathlib import Path


def convert_for_mdbook(content):
    footer = """
---
*The CP-SAT Primer is authored by [Dr. Dominik Krupke](https://github.com/d-krupke) at [TU Braunschweig, Algorithms Group](https://www.ibr.cs.tu-bs.de/alg/index.html). It is licensed under the [CC-BY-4.0 license](https://creativecommons.org/licenses/by/4.0/).*

*The primer is written for educational purposes and does not claim to be complete or correct. If you find this primer helpful, please star the [GitHub repository](https://github.com/d-krupke/cpsat-primer/). As an academic, I also enjoy hearing about how you use CP-SAT to solve real-world problems.*
    """
    content = (
        "<!-- This file was generated by the `build.py` script. Do not edit it manually. -->\n"
        + content
    )
    # replace all inline math `$...$` with `\\( ... \\)` using regex.
    # always use the smallest possible match for the `...` part.
    content = re.sub(r"\$(.*?)\$", r"\\\\( \1 \\\\)", content)
    # replace all math modes "```math ... ```" with `\\[ ... \\]` using regex.
    # always use the smallest possible match for the `...` part.
    content = re.sub(r"```math(.*?)```", r"\\\\[ \1 \\\\]", content, flags=re.DOTALL)
    # replace all `:warning:` with the unicode character for a warning sign.
    content = content.replace(":warning:", "⚠️")
    # replace all anchor links `(#01-installation)` by `(./01_installation.md)`.
    # you have to replace the `#` with `./` and `-` with `_`, and attach `.md` at the end.
    content = re.sub(
        r"\(#(.*?)\)",
        lambda match: "(./" + match.group(1).replace("-", "_") + ".md)",
        content,
    )
    # replace in all links that lead to a .png file the `github.com` with `raw.githubusercontent.com`.
    content = re.sub(
        r"\((.*?\.png)\)",
        lambda match: match.group(0).replace(
            "https://github.com/d-krupke/cpsat-primer/blob/main/",
            "https://raw.githubusercontent.com/d-krupke/cpsat-primer/main/",
        ),
        content,
    )
    content = re.sub(
        r"\((.*?\.gif)\)",
        lambda match: match.group(0).replace(
            "https://github.com/d-krupke/cpsat-primer/blob/main/",
            "https://raw.githubusercontent.com/d-krupke/cpsat-primer/main/",
        ),
        content,
    )
    content = re.sub(
        r"\((.*?\.jpg)\)",
        lambda match: match.group(0).replace(
            "https://github.com/d-krupke/cpsat-primer/blob/main/",
            "https://raw.githubusercontent.com/d-krupke/cpsat-primer/main/",
        ),
        content,
    )

    content += footer
    return content


if __name__ == "__main__":
    # get all markdown files that start with a number
    markdown_files = [f for f in os.listdir() if f.endswith(".md") and f[0].isdigit()]
    markdown_files.sort()

    # concat them and write them to `README.md`
    with open("README.md", "w") as f:
        disclaimer = "<!-- This file was generated by the `build.py` script. Do not edit it manually. -->\n"
        for file in markdown_files:
            with open(file, "r") as current_file:
                content = current_file.read()
                f.write(disclaimer)
                f.write(f"<!-- {file}" + " -->\n")
                f.write(content)
                f.write("\n\n")
                Path("./.mdbook/").mkdir(parents=True, exist_ok=True)
                with open(Path("./.mdbook/") / file, "w") as book_file:
                    book_file.write(convert_for_mdbook(content))
