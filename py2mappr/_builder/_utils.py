import markdown
from markdown3_newtab import NewTabExtension


def md_to_html(md: str) -> str:
    if md is None:
        return ""

    # tab_length is set to 80 to prevent the markdown parser from
    # converting indented text to code blocks
    return markdown.markdown(md, extensions=["fenced_code", NewTabExtension()], tab_length=80)
