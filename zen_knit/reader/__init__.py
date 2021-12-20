import os
from zen_knit.data_types import ReadData, GlobalOption


class BaseReader:
    def __init__(self, input_file, output_file_dir = None) -> None:        
        full_path = self._build_input_file(input_file)
        input_file_path , input_file_name = self._build_input_file_folder(full_path)
        self.raw_data = ReadData(
            global_options=GlobalOption(
                title = "test",
                input_file_dir=input_file_path,
                input_file_name=input_file_name,
                output_file_dir = output_file_dir,
            ),
            data=self._read(full_path)
        )
        
    def _build_input_file(self, input_file):
        return os.path.abspath(input_file)

    def _build_input_file_folder(self, full_path):
        return os.path.split(full_path)

    def _read(self, full_path):
        with open(full_path, "r") as f:
            contents = f.read()
        return contents
        
