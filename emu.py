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
    h1 { font-size: 2.5em; text-align: center;}
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
    li {
        margin-bottom: 0.25em;
    }
    img {
        max-width: 100%;
        height: auto;
        border: 2px solid rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        display: block;
        margin: 0 auto;
    }
"""


def header_replacer(match):
    # Count the number of opening brackets to determine header level
    level = len(match.group(1))
    # Limit the header level to 6
    level = min(level, 6)
    return f"<h{level}>{match.group(2)}</h{level}>"

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

    # headers
    line = re.sub(r"(\[+)([^\[\]]+?)\]+", header_replacer, line)

    # option + keys
    # links (l) - Matches both text and image links
    line = re.sub(r"¬([^|]*?)\|([^|]+?)(?:\|([^|x]+?)x([^|]+?))?(?:\|([^¬]+?))?¬", link_replacer, line)

    # bold (b)
    line = re.sub(r"\∫(.+?)∫", r"<strong>\1</strong>", line)
    # italic (i)
    line = re.sub(r"\ˆ(.+?)ˆ", r"<em>\1</em>", line)

    return line

def link_replacer(match):
    link_text = match.group(1).strip()
    url = match.group(2).strip()
    width = match.group(3).strip() if match.group(3) else None
    height = match.group(4).strip() if match.group(4) else None
    alt_text = match.group(5).strip() if match.group(5) else ""

    # Prepend 'https://' if not present and if it's a web URL
    if url and not (url.startswith(("http://", "https://")) or url.startswith(("/", "./", "../"))):
        url = "https://" + url

    # If the link text is empty, treat it as an image link
    if not link_text:
        size_attr = f' width="{width}" height="{height}"' if width and height else ""
        alt_attr = f' alt="{alt_text}"' if alt_text else ""
        return f'<img src="{url}"{size_attr}{alt_attr}>'

    # For normal text links
    title_attr = f' title="{alt_text}"' if alt_text else ""
    return f'<a href="{url}"{title_attr}>{link_text}</a>'


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


def minify_html(html_content):
    # Simple minification: remove leading/trailing whitespaces and reduce multiple spaces to one
    html_content = re.sub(r">\s+<", "><", html_content)  # Remove whitespace between HTML tags
    html_content = re.sub(r"\s+", " ", html_content)    # Reduce multiple spaces to one
    return html_content


def main():
    if len(sys.argv) != 2:
        print("Usage: emu <filename.emu>")
        sys.exit(1)

    emu_filename = sys.argv[1]
    html_filename = emu_filename.rsplit(".", 1)[0] + ".html"

    with open(emu_filename, "r") as file:
        emu_content = file.read()

    html_content = emu_to_html(emu_content)
    minified_html_content = minify_html(html_content)

    with open(html_filename, "w") as file:
        file.write(minified_html_content)
    print(f"Converted '{emu_filename}' to '{html_filename}'")


if __name__ == "__main__":
    main()
