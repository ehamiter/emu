import re
import sys

DEBUG_MODE = False

# Make this be the default but be swappable with other styles
CSS_STYLES = """
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
        margin: 5px auto;
        padding: 15px 30px;
        line-height: 1.5;
        color: #111;
        background-color: #efefef;
        max-width: 800px;
    }
    blockquote {
        margin: 0;
        padding: 10px 20px;
        background-color: #f9f9f9;
        border-left: 5px solid #ccc;
        position: relative;
        min-height: 2rem;
    }
    :not(blockquote) + blockquote {
        margin-top: 2rem;
    }
    blockquote::before {
        content: '\\201C';
        font-family: serif;
        font-size: 12em;
        color: #ccc;
        position: absolute;
        left: 10px;
        top: 0;
        transform: translateY(-20%);
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
        border: 10px solid white;
        max-width: 100%;
        object-fit: cover;
        height: 100%;
        width: 95%;
    }
    @media (max-width: 600px) {
        img {
            margin: 1em;
        }
    }
    pre.code {
        font-family: monospace;
        background-color: #f0f7ff;
        color: #333333;
        padding: 8px;
        border-radius: 5px;
        border: 1px solid #d1e3f8;
        line-height: 1.5;
        overflow-block: auto;
    }
"""


def debug_print(*args, **kwargs):
    """Print debug messages only if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(*args, **kwargs)


def extract_title(text):
    title_match = re.search(r"†(.*?)†", text)
    if title_match:
        title = title_match.group(1).strip()  # Extract the title
        # Replace the title markup with an HTML comment
        text = re.sub(r"†.*?†", f"<!-- Custom title: {title} -->", text, count=1)
        return title, text
    return "Emu rocks!", text  # Default title if no custom title is found


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


def handle_code_block(text):
    # Use a non-greedy regex to match content between two 'ç' symbols
    code_block_pattern = r"ç(.*?)ç"
    return re.sub(
        code_block_pattern, r"<pre class='code'>\1</pre>", text, flags=re.DOTALL
    )


def handle_image_tag(match):
    url = preprocess_url(match.group(1).strip())
    width = match.group(3).strip() + "px" if match.group(3) else None
    height = match.group(4).strip() + "px" if match.group(4) else None
    alt_text = match.group(5).strip()
    alignment_marker = match.group(6) or "<"

    alignment_style = get_alignment_style(alignment_marker)
    style_attr = build_style_string(alignment_style, width, height)

    img_tag = f'<img src="{url}" style="{style_attr}" alt="{alt_text}">'
    debug_print(f"Image tag: '{img_tag}'")  # Debug print
    return img_tag


def handle_link_tag(match):
    debug_print(f"Link Match groups: {match.groups()}")  # Debug print

    # Check if match groups are not None
    link_text = match.group(1).strip() if match.group(1) else ""
    url = preprocess_url(match.group(2).strip()) if match.group(2) else ""
    title = match.group(3).strip() if match.group(3) else ""

    output = f'<a href="{url}" title="{title}">{link_text}</a>'
    debug_print(f"Link Output: '{output}'")  # Debug print

    return output


def process_emu_line(line):
    debug_print(f"Processing line: {line}")  # Conditional debug print

    if not line.strip():
        return "<p></p>"

    line = re.sub(r"(\[+)([^\[\]]+?)\]+", header_replacer, line)

    # Updated regex pattern for image tags
    image_pattern = r"¬\|([^|]+?)\|?(([^|]*?)x([^|]*?))?\|([^|]*?)\|?([<^>])?¬"
    line = re.sub(image_pattern, handle_image_tag, line)

    # Updated regex pattern for link tags - making it non-greedy
    link_pattern = r"¬([^|]+)\|([^|]+?)(?:\|([^¬]+))?¬"
    line = re.sub(link_pattern, handle_link_tag, line)

    line = re.sub(r"\∫(.+?)∫", r"<strong>\1</strong>", line)
    line = re.sub(r"\ˆ(.+?)ˆ", r"<em>\1</em>", line)

    return line


def get_alignment_style(alignment_marker):
    if alignment_marker == "^":
        return "display: block; margin-left: auto; margin-right: auto;"
    elif alignment_marker == "<":
        return "float: left;"
    elif alignment_marker == ">":
        return "float: right;"
    return ""


def build_style_string(alignment_style, width, height):
    style_parts = []
    if alignment_style:
        style_parts.append(alignment_style)
    if width and height:
        style_parts.append(f"width: {width}; height: {height};")
    style_string = " ".join(style_parts)
    debug_print(f"Style string: '{style_string}'")  # Debug print
    return style_string


def build_image_tag(url, alignment_marker, width, height, alt_text):
    alignment_style = get_alignment_style(alignment_marker)
    style_attr = build_style_string(alignment_style, width, height)
    img_tag = f'<img src="{url}" style="{style_attr}" alt="{alt_text}">'
    debug_print(f"Image tag: '{img_tag}'")  # Debug print
    return img_tag


def build_link_tag(link_text, url, title):
    title_attr = f' title="{title}"' if title else ""
    return f'<a href="{url}"{title_attr}>{link_text}</a>'


def preprocess_url(url):
    # Check if the URL is already complete or is a relative path
    if url.startswith(("http://", "https://", "/", "./", "../")):
        return url
    return "https://" + url


def emu_to_html(emu_text):
    # Step 1: Extract and replace code blocks
    code_blocks = []

    # def extract_code_block(match):
    #     # Trim leading newlines and replace the rest with HTML line break tags
    #     formatted_code = match.group(1).lstrip("\n").replace("\n", "<br>")
    #     code_blocks.append(formatted_code)  # Store the formatted code block
    #     return f"CODE_BLOCK_PLACEHOLDER_{len(code_blocks)-1}"  # Placeholder
    def extract_code_block(match):
        # Extract the code block and split into lines
        code_lines = match.group(1).lstrip("\n").split("\n")
        formatted_lines = []

        for line in code_lines:
            # Replace leading spaces with non-breaking spaces for indentation
            leading_spaces = len(line) - len(line.lstrip(' '))
            formatted_line = '&nbsp;' * leading_spaces + line.lstrip(' ')
            formatted_lines.append(formatted_line)

        formatted_code = "<br>".join(formatted_lines)
        code_blocks.append(formatted_code)  # Store the formatted code block
        return f"CODE_BLOCK_PLACEHOLDER_{len(code_blocks)-1}"  # Placeholder


    emu_text = re.sub(r"ç(.*?)ç", extract_code_block, emu_text, flags=re.DOTALL)

    # Extract title and update emu_text
    title, emu_text = extract_title(emu_text)

    # Process the rest of the document
    emu_text = convert_block_quotes(emu_text)

    # Split the text into lines and process each line
    lines = emu_text.split("\n")
    processed_lines = []
    for line in lines:
        processed_line = process_emu_line(line)
        processed_lines.append(processed_line)

    # Reassemble the processed text
    emu_text = "".join(processed_lines)

    # Step 3: Reinsert code blocks
    for i, code in enumerate(code_blocks):
        placeholder = f"CODE_BLOCK_PLACEHOLDER_{i}"
        emu_text = emu_text.replace(placeholder, f"<pre class='code'>{code}</pre>")

    # Final HTML assembly
    html_output = f"""
        <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{title}</title><meta charset="UTF-8"><style>{CSS_STYLES}</style></head><body>
        {emu_text}
        </body></html>
    """
    return html_output

def minify_html(html_content):
    # Simple minification: remove leading/trailing whitespaces and reduce multiple spaces to one
    html_content = re.sub(
        r">\s+<", "><", html_content
    )  # Remove whitespace between HTML tags
    html_content = re.sub(r"\s+", " ", html_content)  # Reduce multiple spaces to one
    return html_content


def main():
    if len(sys.argv) != 2:
        debug_print("Usage: emu <filename.emu>")
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
