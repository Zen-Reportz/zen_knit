import io

from nbconvert import filters
from pygments.formatters import LatexFormatter
from subprocess import Popen, PIPE
from pygments import highlight
from IPython.lib.lexers import IPyLexer
from pygments.formatters import LatexFormatter

from zen_knit.data_types import ChunkOption, GlobalOption, OrganizedChunk, OrganizedData
from zen_knit.formattor.base_formatter import BaseFormatter

class TexFormatter(BaseFormatter):
    def __init__(self, organized_data:OrganizedData):
        super().__init__(organized_data)
        self.header = ("""\\documentclass[a4paper,11pt,final]{article}
            \\usepackage{fancyvrb, color, graphicx, hyperref, amsmath, url, textcomp, booktabs}
            \\usepackage{palatino}
            \\usepackage[a4paper,text={16.5cm,25.2cm},centering]{geometry}

            %%Set different options for xetex and luatex
            \\usepackage{iftex}
            \\ifxetex\\usepackage{fontspec}\\fi

            \\ifluatex\\usepackage{fontspec}\\fi

            \\usepackage{xcolor}
            %% ANSI colors from nbconvert
            \\definecolor{ansi-black}{HTML}{3E424D}
            \\definecolor{ansi-black-intense}{HTML}{282C36}
            \\definecolor{ansi-red}{HTML}{E75C58}
            \\definecolor{ansi-red-intense}{HTML}{B22B31}
            \\definecolor{ansi-green}{HTML}{00A250}
            \\definecolor{ansi-green-intense}{HTML}{007427}
            \\definecolor{ansi-yellow}{HTML}{DDB62B}
            \\definecolor{ansi-yellow-intense}{HTML}{B27D12}
            \\definecolor{ansi-blue}{HTML}{208FFB}
            \\definecolor{ansi-blue-intense}{HTML}{0065CA}
            \\definecolor{ansi-magenta}{HTML}{D160C4}
            \\definecolor{ansi-magenta-intense}{HTML}{A03196}
            \\definecolor{ansi-cyan}{HTML}{60C6C8}
            \\definecolor{ansi-cyan-intense}{HTML}{258F8F}
            \\definecolor{ansi-white}{HTML}{C5C1B4}
            \\definecolor{ansi-white-intense}{HTML}{A1A6B2}

            \\hypersetup
            {   pdfauthor = {Pweave},
                pdftitle={Published from %s},
                colorlinks=TRUE,
                linkcolor=black,
                citecolor=blue,
                urlcolor=blue
            }
            \\setlength{\parindent}{0pt}
            \\setlength{\parskip}{1.2ex}
            %% fix for pandoc 1.14
            \\providecommand{\\tightlist}{%%
                \\setlength{\\itemsep}{0pt}\\setlength{\\parskip}{0pt}}
            %s
            """) % (self.organized_data.global_options.input_file_name, LatexFormatter().get_style_defs())
        self.formatted_doc = ''
        self.footer = r"\end{document}"
        self.subheader = "\n\\begin{document}\n"


    def _parsetitle(self, global_option:GlobalOption):
        title = global_option.title
        author = global_option.author
        date = global_option.date
        self.header += f'\n\\title{{{title}}}\n'
        if author is not None:
            self.header += f'\\author{{{author}}}\n'
        if date is not None:
            self.header += f'\\date{{{date}}}\n' 
        self.subheader += "\maketitle\n"
        
    def _format_docchunk(self, content:OrganizedChunk):
        if "tabular" in content.str_data:
            all_data = content.str_data.split("\\n")
            all_data = [t.replace("\n", "").replace("\\\\", "\\")  for t in all_data ]
            all_data = "\n".join(all_data)
        else:
            all_data = content.str_data
            
      
        try:
            pandoc = Popen(["pandoc", "-t", "latex+raw_tex", "-f", "markdown"], stdin=PIPE, stdout=PIPE)
        except:
            raise Exception("ERROR: Can't find pandoc")
        pandoc.stdin.write(all_data.encode('utf-8'))
        transfomed = pandoc.communicate()[0].decode('utf-8')
        return transfomed
    

    def _format_codechunks(self, content:OrganizedChunk):
        transfomed = content.str_data
        transfomed = highlight(transfomed, IPyLexer(), LatexFormatter(verboptions="frame=single,fontsize=\small, xleftmargin=0.5em"))
        transfomed = filters.ansi2latex(transfomed)
        return transfomed

    def _format_image(self, content:OrganizedChunk):

        result = ""
        figstring = ""

        options: ChunkOption   
        options = content.complex_data["options"]
        fig_width =  options.fig_width or "\linewidth"
        fig_caption = options.fig_caption
        fig_env = options.fig_env
        fig_position = options.fig_position
        name =  options.name
        
        if fig_env is not None:
            result += f"\\begin{{{fig_env}}}\n"

        for fig in content.complex_data["plots"]:
            figstring += f"\\includegraphics[width= {fig_width}]{{{fig}}}\n" 

        # Figure environment
        if fig_caption:
            result += f"""\\begin{{figure}}[{fig_position}]
                       \\center
                       {figstring}
                       "\\caption{fig_caption}\n"""
            if name:
                result += f"\label{{fig:{name}}}\n" 
            result += "\\end{figure}\n"

        else:
            result += figstring

        if fig_env is not None:
            result += f"\\end{{{fig_env}}}\n"

        return result
    
    def _build_doc(self):
        self.formatted_doc =  self.header  + self.subheader  + self.formatted_doc + self.footer

    def write_file(self):
        fd = self.organized_data.global_options.output_file_dir
        fn = self.organized_data.global_options.output_file_name.split(".")[0] + ".tex"
        file_  = f"{fd}/{fn}"
        with io.open(file_, 'wt', encoding='utf-8') as f:
            f.write(self.formatted_doc)

        return file_

    def _post_process(self, file_):
        try:
            # pandoc2latex
            # pdflatex
            latex = Popen(["pdflatex", "-output-directory", self.organized_data.global_options.output_file_dir, file_], stdin=PIPE, stdout=PIPE)
            print("Running  pdflatex ...")
        except Exception as e:
            print(e)
            print("Can't find pdflatex no pdf produced!")
            return
        x = latex.communicate()[0].decode('utf-8')
        print("\n".join(x.splitlines()[-2:]))