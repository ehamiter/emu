import re
import sys

CSS_STYLES = """
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
        margin: 5px auto;
        padding: 15px 30px;
        line-height: 1.25;
        color: #333;
        background-color: #fdfdfd;
        max-width: 800px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    blockquote {
        margin: 0 0 0 5px;
        padding: 10px 20px;
        background-color: #f9f9f9;
        border-left: 5px solid #ccc;
        position: relative;
    }
    :not(blockquote) + blockquote {
        margin-top: 2rem;
    }
    blockquote::before {
        content: '\\201C';
        font-size: 4em;
        color: #ccc;
        position: absolute;
        left: 10px;
        top: -10px;
        opacity: 0.3;
    }
    blockquote.nested {
        margin-left: 1.25rem;
    }
    h1, h2, h3, h4, h5, h6 {
        margin-top: 1em;
        margin-bottom: 0.5em;
        font-weight: normal;
        line-height: 1.25;
        color: #333;
    }
    h1 { font-size: 2em; }
    h2 { font-size: 1.75em; }
    h3 { font-size: 1.5em; }
    h4 { font-size: 1.25em; }
    h5 { font-size: 1.125em; }
    h6 { font-size: 1em; }
    a {
        color: #0077cc;
        text-decoration: none;
        border-bottom: 2px solid #0077cc;
        transition: color 0.3s ease, border-bottom-color 0.3s ease;
    }
    a:hover, a:focus {
        color: #005fa3;
        border-bottom-color: #005fa3;
    }
    p {
        margin-top: 0;
        margin-bottom: 0.5em;
    }
    ul, ol {
        margin-top: 0;
        margin-bottom: 0.5em;
        padding-left: 20px;
    }
    li { margin-bottom: 0.25em;
    }
"""


def header_replacer(match):
    # Count the number of opening brackets to determine header level
    level = len(match.group(1))
    # Limit the header level to 6
    level = min(level, 6)
    return f"<h{level}>{match.group(2)}</h{level}>"


def link_replacer(match):
    link_text = match.group(1)
    url = match.group(2)
    title = match.group(3)

    # Prepend 'https://' if not present
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Include title if provided
    title_attr = f' title="{title}"' if title else ""

    return f'<a href="{url}"{title_attr}>{link_text}</a>'


def convert_block_quotes(text):
    while "{{" in text:
        text = re.sub(
            r"\{\{(.*?)\}\}",
            r'<blockquote class="nested">\1</blockquote>',
            text,
            flags=re.DOTALL,
        )
    text = re.sub(r"\{(.*?)\}", r"<blockquote>\1</blockquote>", text, flags=re.DOTALL)
    return text


def process_emu_line(line):
    # Check if the line is empty and create a paragraph
    if not line.strip():
        return "<p></p>"
    # Process headers, links, bold, and italic
    line = re.sub(r"(\[+)([^\[\]]+?)\]+", header_replacer, line)
    line = re.sub(r"¬(.+?)\|(.+?)(?:\|(.+?))?¬", link_replacer, line)
    line = re.sub(r"\∫(.+?)\∫", r"<strong>\1</strong>", line)
    line = re.sub(r"\ˆ(.+?)\ˆ", r"<em>\1</em>", line)
    return line


def emu_to_html(emu_text):
    html_output = f"<html><head><style>{CSS_STYLES}</style></head><body>"
    emu_text = convert_block_quotes(emu_text)

    # Split the text into lines and process each line
    lines = emu_text.split("\n")
    processed_lines = []
    for i, line in enumerate(lines):
        processed_line = process_emu_line(line)
        # No need to add <br> tags as paragraphs are now handled
        processed_lines.append(processed_line)

    html_output += "".join(processed_lines)
    html_output += "</body></html>"
    return html_output


def main():
    if len(sys.argv) != 2:
        print("Usage: emu <filename.emu>")
        sys.exit(1)

    emu_filename = sys.argv[1]
    html_filename = emu_filename.rsplit(".", 1)[0] + ".html"

    with open(emu_filename, "r") as file:
        emu_content = file.read()

    html_content = emu_to_html(emu_content)

    with open(html_filename, "w") as file:
        file.write(html_content)
    print(f"Converted '{emu_filename}' to '{html_filename}'")


if __name__ == "__main__":
    main()
