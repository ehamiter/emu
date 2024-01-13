import re
import sys

def emu_to_html(emu_text):
    """
    [This is a big title (h1)]

    [[This is a level two heading (h2)]]

    [[[This is a level three heading (h3)]]]

    [[[[Level four heading (h4)]]]]

    [[[[[Level five heading (h5)]]]]]

    [[[[[[Level six heading (h6)]]]]]]

    `Click on a link | https://webpage.com`

    !!Bold text!!

    !Italicized text!

    { This is a block quote. }
    {{ Nested block quote. }}
    """

    # Function to determine header level based on bracket count
    def header_replacer(match):
        # Count the number of opening brackets to determine header level
        level = len(match.group(1))
        # Limit the header level to 6
        level = min(level, 6)
        return f'<h{level}>{match.group(2)}</h{level}>'

    # Regular expression for headers
    # Matches text like '[text]', '[[text]]', up to '[[[[[[text]]]]]]'
    emu_text = re.sub(r'(\[+)([^\[\]]+?)\]+', header_replacer, emu_text)

    # Other EMU syntax replacements
    emu_text = re.sub(r'`(.+?)\|(.+?)`', r'<a href="\2">\1</a>', emu_text)
    emu_text = re.sub(r'\!\!(.+?)\!\!', r'<strong>\1</strong>', emu_text)
    emu_text = re.sub(r'\!(.+?)\!', r'<em>\1</em>', emu_text)
    emu_text = convert_block_quotes(emu_text)

    return emu_text

def convert_block_quotes(text):
    # Inline styles for block quotes
    base_style = 'margin: 20px; padding: 10px; border-left: 3px solid #ccc; background-color: #f9f9f9;'
    nested_style = f'{base_style} margin-left: 30px;'

    while '{{' in text:
        text = re.sub(r'\{\{(.*?)\}\}', rf'<blockquote style="{nested_style}">\1</blockquote>', text, flags=re.DOTALL)
    text = re.sub(r'\{(.*?)\}', rf'<blockquote style="{base_style}">\1</blockquote>', text, flags=re.DOTALL)

    return text


def main():
    if len(sys.argv) != 2:
        print("Usage: emu <filename.emu>")
        sys.exit(1)

    emu_filename = sys.argv[1]
    html_filename = emu_filename.rsplit('.', 1)[0] + '.html'

    with open(emu_filename, 'r') as file:
        emu_content = file.read()

    html_content = emu_to_html(emu_content)

    with open(html_filename, 'w') as file:
        file.write(html_content)
    print(f"Converted '{emu_filename}' to '{html_filename}'")

if __name__ == "__main__":
    main()
