import io
from zen_knit.data_types import OrganizedData, GlobalOption, OrganizedChunk



class BaseFormatter:
    def __init__(self, organized_data: OrganizedData):
        self.organized_data = organized_data
        self.formatted_doc = ""
        self.header = ""
        self.footer = ""
        self.subheader = ""


    def run(self):
        self._parsetitle(self.organized_data.global_options)
        self._format_doc()
        self._build_doc()
        file_ = self.write_file()
        self._post_process(file_)

    
    def _parsetitle(self, global_option:GlobalOption):
        pass

    def _format_docchunk(self, content:OrganizedChunk):
        pass
    
    def _format_codechunks(self, content:OrganizedChunk):
        pass
    
    def _format_image(self, content:OrganizedChunk):
        pass

    def _build_doc(self):
        pass 
    
    def _format_doc(self):
        chunk: OrganizedChunk
        for chunk in self.organized_data.chunks:
            if chunk.type == "markdown":
                t = self._format_docchunk(chunk)
                self.formatted_doc = self.formatted_doc + "\n" + t
            elif chunk.type == "code":
                t = self._format_codechunks(chunk)
                self.formatted_doc = self.formatted_doc + "\n" + t
            elif chunk.type == "se_data":
                t = self._format_codechunks(chunk)
                self.formatted_doc = self.formatted_doc + "\n" + t
            elif chunk.type == "e_data":
                t = self._format_docchunk(chunk)
                self.formatted_doc = self.formatted_doc + "\n" + t
            elif chunk.type == "plot":
                t = self._format_image(chunk)
                self.formatted_doc = self.formatted_doc + "\n" + t
            else:
                print("Not right format")

    def write_file(self):
        fd = self.organized_data.global_options.output_file_dir
        fn = self.organized_data.global_options.output_file_name
        file_  = f"{fd}/{fn}"
        with io.open(file_, 'wt', encoding='utf-8') as f:
            f.write(self.formatted_doc)
        
    def _post_process(self, file_):
        pass
    #     markdown_file = self.executed_data.global_options.input_file_name.split(".")[0] + ".md"
    #     markdown_file = os.path.join(self.executed_data.global_options.output_file_dir , markdown_file)
    #     with open(markdown_file, "w") as f:
    #         text = "\n".join(self.formatted_doc)
    #         f.write(text)
                