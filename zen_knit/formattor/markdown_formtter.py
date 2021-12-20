import io
from nbconvert import filters
from zen_knit.data_types import ChunkOption, ExecutedData, GlobalOption, OrganizedChunk
from zen_knit.formattor.base_formatter import BaseFormatter


class MarkDownFormatter(BaseFormatter):
    def __init__(self, executed_data: ExecutedData):
        self.formatted_doc = []
        self.header = ""
    
    def _parsetitle(self, global_option:GlobalOption):
        title = global_option.title
        author = global_option.author
        date = global_option.date
        self.header += f"% {title}"
        if author is not None:
            self.header += f"% {author}"
        if date is not None:
            self.header += f"% {date}"

    def _format_docchunk(self, content:OrganizedChunk):
        return content.str_data
    
        
    def _format_codechunks(self, content:OrganizedChunk):
        t = content.str_data
        if content.type == "code":
            return f"```python \n {t} \n ```"
        else:
            return f"``` \n {t} \n ```"

    def _format_image(self, content:OrganizedChunk):
        result = ""
        figstring = ""
        options: ChunkOption
        options = content.complex_data["options"]
        for fig in content.complex_data["plot"]:
            if options.fig_caption:
                result += f"[{options.fig_caption}][{fig}]"
            else:
                result += f"[][{fig}]"

        return result
    

    def _build_doc(self):
        self.formatted_doc =  self.header + self.formatted_doc
        
    def write_file(self):
        fd = self.organized_data.global_options.output_file_dir
        fn = self.organized_data.global_options.output_file_name
        file_  = f"{fd}/{fn}"
        with io.open(file_, 'wt', encoding='utf-8') as f:
            f.write(self.formatted_doc)
        

    #     markdown_file = self.executed_data.global_options.input_file_name.split(".")[0] + ".md"
    #     markdown_file = os.path.join(self.executed_data.global_options.output_file_dir , markdown_file)
    #     with open(markdown_file, "w") as f:
    #         text = "\n".join(self.formatted_doc)
    #         f.write(text)
                