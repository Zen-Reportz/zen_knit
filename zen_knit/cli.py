import os
import click

from zen_knit.executor import BaseExecutor
from zen_knit.formattor import get_formatter
from zen_knit.formattor.base_formatter import BaseFormatter
from zen_knit.organizer import BaseOrganizer
from zen_knit.parser import BaseParser
from zen_knit.reader import BaseReader

@click.command()
@click.option("-f", '--file', help='Pyz file name with path or file name for current dirctory', required=True)
@click.option("-ofd", '--output_file_dir', help='where output you want to put it, if not provided, current working directory will be used')
def knit(file, output_file_dir):
    if output_file_dir is None:
        output_file_dir = os.getcwd()

    output_file_dir = os.path.abspath(output_file_dir)
    file = os.path.abspath(file)

    br = BaseReader(file, output_file_dir)
    bp = BaseParser(br.raw_data)
    be = BaseExecutor(bp.parsed_data)
    bo = BaseOrganizer(be.excuted_data)
    f = get_formatter(bo.organized_data.global_options.output_format)
    bf:BaseFormatter # or its derivative class
    bf = f(bo.organized_data)
    bf.run()