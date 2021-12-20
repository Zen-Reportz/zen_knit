from pydantic import BaseModel, validator
from typing import List, Optional, Tuple, Any



class GlobalOption(BaseModel):
    title: str
    author: Optional[str]
    date: Optional[str]
    input_file_dir: str
    input_file_name: str
    matplot: bool = True
    kernal: str = "python3"
    log_level: str = "debug"
    fig_dir: str = "figures"
    css: str = "bootstrap"
    output_format: Optional[str]
    output_file_name: Optional[str]
    output_file_dir: Optional[str]
    
    @validator('log_level')
    def fix_option_for_log(cls, v:str):
        if v.lower() not in ('notset', "debug", 'info', 'warning', 'error', 'critical'):
            raise ValueError('must contain a space')
        return v.title()



class ChunkOption(BaseModel):
    name: Optional[str]
    output: str = "pdf"
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