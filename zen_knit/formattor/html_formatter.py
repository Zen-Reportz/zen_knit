import base64
import requests
from zen_knit.formattor import html_support
try:
    import markdown
except ImportError:
    message = "You'll need to install python markdown in order to use markdown to html formatter\nrun 'pip install markdown' to install"
    print(message)
from nbconvert import filters
from pygments import highlight
from IPython.lib.lexers import IPyLexer
from pygments.formatters import HtmlFormatter
from zen_knit.data_types import ChunkOption, OrganizedData, GlobalOption, OrganizedChunk
from zen_knit.formattor.base_formatter import BaseFormatter
from zen_knit.formattor.makrdown_math import MathExtension
from zen_knit.formattor.html_support import htmltemplate, themes
from zen_knit import __version__
import os

class HTMLFormatter(BaseFormatter):
    def __init__(self, organized_data:OrganizedData):
        super().__init__(organized_data)

    @staticmethod
    def _make_css_request(url):
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception(f"CSS URL dont found, status code is {r.status_code}")
        if 200 < r.status_code < 300:
            print(f"css get request return status code {r.status_code}")

        return r.text

    @staticmethod
    def _get_default_theme(css):
        theme_css = themes.get(css)
        return theme_css
        
    def _get_css(self):
        css = self.organized_data.global_options.output.html.css
        if 'http' in css:
            return self._make_css_request(css)
        
        results = self._get_default_theme(css)
        
        if results is None:
            file = os.path.abspath(css)
            with open(file, "r") as f:
                results = f.read()

        if results is None:
            raise Exception(f"No CSS found in default themes and file, , currently we are supporting {themes.keys()} ")
            
        return results
    
    def _add_header_fotter(self):
        theme_css = self._get_css()
        self.header = (htmltemplate["header"] %
                {"pygments_css"  : HtmlFormatter().get_style_defs(),
                "theme_css" : theme_css})
        self.footer = htmltemplate["footer"].format(source=self.organized_data.global_options.input.file_name, version=__version__, date=self.organized_data.global_options.date)

    def _parsetitle(self, global_option:GlobalOption):
        self._add_header_fotter()
        title = global_option.title
        author = global_option.author
        date = global_option.date
        lines = ''
        lines += f'\n <H1 class = "title", id="ttitle">{title}</H1> <BR/>'
        if author is not None:
            lines += f'\n <strong>Author:</strong> {author} <BR/>'
        if date is not None:
            lines += f'\n <strong>Date:</strong> {date} <BR/>' 
        
        self.header += lines        

    def _format_docchunk(self, content:OrganizedChunk):
        t = "\n".join(content.str_data.split("\\n"))
        return markdown.markdown(t, extensions=[MathExtension()])
    
    def _format_codechunks(self, content:OrganizedChunk):
        t = filters.ansi2html(content.str_data)
        t = highlight(t, IPyLexer(), HtmlFormatter())

        return t

    def _format_html(self, content: OrganizedChunk):
        if '<table' in content.str_data:
            return "\n".join(content.str_data.split("\\n"))
        else:
            return content.str_data
    
    def _format_image(self, content:OrganizedChunk):
        result = ""
        figstring = ""
        options: ChunkOption
        options = content.complex_data["options"]
        for fig in content.complex_data["plots"]:
            with open(fig, "rb") as f:
                data = f.read()
            fig_base64 = base64.b64encode(data).decode("utf-8")
            figstring += f'<img src="data:image/png;base64,{fig_base64}" width="{options.fig_width}"/>\n' 

        if options.fig_caption:
            if options.name:
                labelstring = f'data-label = "fig:{options.name}"' 
            else:
                labelstring = ""

            result += f"""<figure>
                       {figstring}
                       "<figcaption {labelstring}>{options.fig_caption}</figcaption>\n</figure>"""

        else:
            result += figstring

        return result

    def _build_doc(self):
        self.formatted_doc =  self.header + self.formatted_doc  + self.footer
    
  