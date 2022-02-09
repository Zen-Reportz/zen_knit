
import enum
from pydantic import BaseModel, validator
from typing import List, Optional, Tuple, Any


class Input(BaseModel):
    dir: Optional[str]
    file_name: Optional[str]
    matplot: bool = True

class latexOuput(BaseModel):
    header: Optional[str] 
    page_size: Optional[str] = 'a4paper'
    geometry_parameters: Optional[str] = "text={16.5cm,25.2cm},centering"
    
class htmlOutput(BaseModel):
    css: str = "bootstrap"

class Output(BaseModel):
    fig_dir: str = "figures"
    format: Optional[str]
    file_name: Optional[str]
    dir: Optional[str]
    latex: Optional[latexOuput]
    html: Optional[htmlOutput]


class GlobalOption(BaseModel):
    title: str
    author: Optional[str]
    date: Optional[str]
    kernal: str = "python3"
    log_level: str = "debug"
    cache: Optional[bool] = False
    output: Output
    input: Input

    @validator('log_level')
    def fix_option_for_log(cls, v:str):
        if v.lower() not in ('notset', "debug", 'info', 'warning', 'error', 'critical'):
            raise ValueError('must contain a space')
        return v.title()



class ChunkOption(BaseModel):
    name: Optional[str]
    echo: bool = True
    render: bool = True
    run: bool = True
    fig: bool =  False
    fig_size: Tuple =  (6, 4)
    fig_dpi: int = 200
    fig_caption: Optional[str] 
    fig_position: Optional[str] = "htpb"
    fig_env: Optional[str]
    fig_width: Optional[str]
    con_string: Optional[str] = "zen_con"

BOOLENCHUNCKOPTIONS = ['run', 'echo','render', 'fig']


class Chunk(BaseModel):
    type: str
    string_: str
    options: Optional[ChunkOption]


class ParseData(BaseModel):
    global_options: Optional[GlobalOption]
    chunks: List[Chunk]

class ReadData(BaseModel):
    global_options: Optional[GlobalOption]
    data: str


class ExecuatedChucnkOut(BaseModel):
    output_type: str
    data: dict

class ExecuatedChunk(BaseModel):
    chunk: Chunk
    results: List[ExecuatedChucnkOut]

class ExecutedData(BaseModel):
    global_options: Optional[GlobalOption]
    chunks: List[ExecuatedChunk]


class OrganizedChunk(BaseModel):
    type: str
    str_data: str = ""
    complex_data: dict = {}


class OrganizedData(BaseModel):
    global_options: Optional[GlobalOption]
    chunks: List[OrganizedChunk]

class OrganizedChuckType(enum.Enum):
    Markdown = "markdown"
    Code = "code"
    Result = "se_data"
    Table = "e_data"
    HTML = "html_data"
    Plot = "plot"
            