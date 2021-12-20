from io import RawIOBase
from posixpath import split
import re
import datetime
import ast
from zen_knit.data_types import GlobalOption, ReadData, ChunkOption, Chunk, ParseData, BOOLENCHUNCKOPTIONS

def option_parser(raw: str) -> ChunkOption:
    options = raw.split("{")[1].split("}")[0].replace(" ", "").split(",")
    option_dict = {}
    for option in options:
        if "=" not in option :
            continue
        passed_option, value = option.split("=")
        if passed_option in BOOLENCHUNCKOPTIONS:
            value = (value == "true") or (value == "True") or (value == "t") or (value == "T")
        option_dict[passed_option] = value
    selected_options = ChunkOption(**option_dict)
    return selected_options


class BaseParser:
    
    def __init__(self, data:ReadData) -> None:
        self.raw_data = data
        self.parsed_data = None
        self.starter_line = "^```\{.*?\}\s*$"
        self.ender_line = "^```$"
        self.title_info = {}
        self._parse_data()

    def _parse_title(self, title_info):
        title_present = False
        for t in title_info.splitlines():
            split_t = t.split(":")
            
            if len(split_t) == 2:
                split_t[1] = split_t[1].lstrip()
                if "title" == split_t[0]:
                    self.raw_data.global_options.__setattr__("title", split_t[1])
                    title_present = True
                if "author" == split_t[0]:
                    self.raw_data.global_options.__setattr__("author", split_t[1])
                if "date" == split_t[0]:
                    date1 = split_t[1]
                    if  "CURRENT_DATE" in date1:
                        date1 =  datetime.datetime.now().strftime("%d %B, %Y")
                    elif "datetime" in date1:
                        date1 = eval(date1)
                    self.raw_data.global_options.__setattr__("date", date1)
                if "output" == split_t[0]:
                    self.raw_data.global_options.__setattr__("output_format", split_t[1])
            else:
                raise Exception("Not right information in title place")
        
        if (not title_present) and (self.raw_data.global_options.title == "test"):
            raise Exception("Title is not provided")

    def _parse_data(self):
        started = False
        current_strings = []
        temp_string = ''
        type_ = None
        option = option_parser("{}")
        if re.match("^---$", self.raw_data.data[:3]):
            _, title, raw_data = re.split("---\n", self.raw_data.data)
            self._parse_title(title)
        else:
            raw_data = self.raw_data.data
        for _, raw in enumerate(raw_data.splitlines()):
            if re.match(self.starter_line, raw):
                if started:
                    raise Exception("code is already started")
                else:
                    current_strings.append(Chunk(type= 'text' if type_ is None else type_,
                                                 string_= temp_string, 
                                                 options= option))
                    temp_string = ''
                    started = True
                    type_ = 'code'
                    option = option_parser(raw)

            else:
                if re.match(self.ender_line, raw):
                    if started:
                        current_strings.append(Chunk(type= 'text' if type_ is None else type_,
                                                 string_= temp_string, 
                                                 options= option))
                        temp_string = ''
                        started = False
                        type_ = None
                        option = option_parser("{}")
                        

                    else:
                        raise Exception("code is not started")
                else:
                    if temp_string != "":
                        temp_string = temp_string + "\n" + raw
                    else:
                        temp_string = raw
        
        current_strings.append(Chunk(type= 'text' if type_ is None else type_,
                                                 string_= temp_string, 
                                                 options= option))

        self.parsed_data = ParseData(global_options=self.raw_data.global_options, chunks=current_strings)
