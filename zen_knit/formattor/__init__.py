from zen_knit.formattor.base_formatter import BaseFormatter
from zen_knit.formattor.html_formatter import HTMLFormatter
from zen_knit.formattor.markdown_formtter import MarkDownFormatter
from zen_knit.formattor.tex_formatter import TexFormatter

mime_extensions = {"image/png" : "png",
                   "image/jpg" : "jpg"}


my_formatter = {"pdf": TexFormatter,
            "html": HTMLFormatter,
            "markdown":MarkDownFormatter}


def get_formatter(output) -> BaseFormatter:
    return my_formatter[output]