import re
from zen_knit.data_types import GlobalOption, ReadData, ChunkOption, Chunk, ParseData, BOOLENCHUNCKOPTIONS
import oyaml
import datetime

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                print(f"over writing deafult value for {key}")
                a[key] = b[key]

        else:
            a[key] = b[key]
    return a


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
        old_data = self.raw_data.global_options.dict()
        new_data = oyaml.safe_load(title_info)
        final_data = merge(old_data, new_data)
        if  "CURRENT_DATE" in final_data["date"]:
            date1 =  datetime.datetime.now().strftime("%d %B, %Y")
        elif "datetime" in final_data["date"]:
            date1 = eval(final_data["date"])
        final_data["date"] = date1

        self.raw_data.global_options = GlobalOption(**final_data)


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
                    if ('{sql' in raw.lower()):
                        type_ = 'sql'
                    else:
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
