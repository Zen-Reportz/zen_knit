import io
import os
import base64
from pathlib import Path

from nbconvert import filters
from pygments.formatters.latex import LatexFormatter
from zen_knit import formattor

from zen_knit.data_types import ChunkOption, ExecutedData, OrganizedChunk, OrganizedData
from zen_knit.formattor.html_formatter import HTMLFormatter


mime_extensions = {"image/png" : "png",
                   "image/jpg" : "jpg"}


class BaseOrganizer:
    def __init__(self, executed_data: ExecutedData):
        self.format_started = False
        self.collected_string = ""
        self.fig_folder = None
        self.executed_data = executed_data
        self.formatted_doc = []
        self.organized_data = OrganizedData(
            global_options = self.executed_data.global_options,
            chunks = []
        )
        self._create_output_folder_name()
        self._create_fig_folder()
        self._organize_doc()
        self._create_output_file_name()

    def _create_output_file_name(self):
        global_options = self.organized_data.global_options
        global_options.output_file_name = global_options.input_file_name.split(".")[0] + "."+ global_options.output_format

      
    def _create_output_folder_name(self):
        global_options = self.organized_data.global_options
        
        if global_options.output_file_dir is None:
            global_options.output_file_dir = global_options.input_file_dir
        

    def _create_fig_folder(self):
        output_folder = self.organized_data.global_options.output_file_dir
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        fig_folder = os.path.join(output_folder, self.organized_data.global_options.fig_dir)
        self.fig_folder = fig_folder
        Path(fig_folder).mkdir(parents=True, exist_ok=True)
    

    def _parse_raw(self, data, output_type):
        if data.get("code_text_raw") is not None:
            if self._clean_up(data['code_text_raw']) is not None:
                if output_type == "code":
                    t = {"type": "code", "str_data": data['code_text_raw'] }
                else:
                    t = {"type": "markdown", "str_data": data['code_text_raw'] }
                
                self.organized_data.chunks.append(OrganizedChunk(**t))
            return True
        else:
            return False
    
    
        
    def _coder_string(self, data):
        list_ = ["stream", "error"]
        if data["output_type"] is None:
            return False
        

        if data["output_type"] in list_:
            if data["output_type"] == "stream":
                if self._clean_up(data['text']) is not None:
                    t = {"type": "se_data", "str_data": data['text'] }
                    self.organized_data.chunks.append(OrganizedChunk(**t))

            if data["output_type"] == "error":
                t = {"type": "se_data", "str_data": data["evalue"] + filters.strip_ansi("".join(data["traceback"])) }
                self.organized_data.chunks.append(OrganizedChunk(**t))

            return True

        return False

    def _raw_string(self, data):
        if data["output_type"] is None:
            return False


        if data["output_type"] == "execute_result":
            if data.get("data") is not None:
                if 'matplotlib' in data["data"]["text/plain"]:
                    # Doing nothing here
                    return True
                else:
                    if ((data["data"]["text/plain"][0] == "'") or (data["data"]["text/plain"][0] == '"')):
                        temp = data["data"]["text/plain"][1:-1]
                    else:
                        temp = data["data"]["text/plain"]
                    
                    if self._clean_up(temp) is not None:
                        t = {"type": "e_data", "str_data":temp }
                        self.organized_data.chunks.append(OrganizedChunk(**t))
                    
                    return True
        
            return True           

        return False
    
    def _raw_plots(self, data, chunk_option:ChunkOption):
        if data["output_type"] is None:
            return False

        if data["output_type"] == "display_data":
            plot_infos = self._save_plots(data, chunk_option)
            t = {"type": "plot", "complex_data":{"plots": plot_infos, "options": chunk_option }}
            self.organized_data.chunks.append(OrganizedChunk(**t))
            return True
        return False
    
    def _save_plots(self, data, chunk_option:ChunkOption):
        figs = []
        i = 1
        for m in mime_extensions:
            if m in data["data"]:
                fig_full_path, fig_relative_path = self._build_file(mime_extensions[m], i, chunk_option.fig_caption, chunk_option.name)
                figs.append(fig_relative_path)
                bfig = base64.b64decode(data["data"][m])
                with open(fig_full_path, "wb") as f:
                    f.write(bfig)
                i += 1
        return figs
    
    def _build_file(self, extension, index, fig_caption= None, name =None):
        
      
        fig_name = ""
        if fig_caption is not None:
            fig_name = fig_name + "_" +  fig_caption

        if name is not None:
            fig_name = fig_name + "_" + name
        
        fig_name = fig_name + "_" + str(index)
        fig_name = fig_name + "." + extension
        return  os.path.join(self.fig_folder, fig_name), os.path.join(self.fig_folder, fig_name)

    def _organize_doc(self):
        for chunk in self.executed_data.chunks:
            chunk_option = chunk.chunk.options
            results = chunk.results
            for result in results:
                data = result.data
                present = self._parse_raw(data, result.output_type)
                if present:
                    continue
                present = self._coder_string(data)
                if present:
                    continue
               
                present = self._raw_string(data)
                if present:
                    continue

                present = self._raw_plots(data, chunk_option)
                if present:
                    continue
                print("not supported format", data)
            
        
        t = []
        c: OrganizedChunk
        for c in self.organized_data.chunks:
            last_chank: OrganizedChunk
            if len(t)> 0:
                last_chank = t[-1]
            else:
                last_chank = None
            
            if last_chank is None:
                t.append(c)
            else:
                if (c.type == last_chank.type) & (c.type != "plot"):
                    last_chank.str_data = last_chank.str_data + "\n" + c.str_data
                else:
                    t.append(c)
        self.organized_data.chunks = t
    
    @staticmethod
    def _clean_up(doc):
        d = doc.replace(" ", "").replace("\n", "")
        if len(d) != 0:
            return doc
        else:
            return None
        

    #     markdown_file = self.executed_data.global_options.input_file_name.split(".")[0] + ".md"
    #     markdown_file = os.path.join(self.executed_data.global_options.output_file_dir , markdown_file)
    #     with open(markdown_file, "w") as f:
    #         text = "\n".join(self.formatted_doc)
    #         f.write(text)
                