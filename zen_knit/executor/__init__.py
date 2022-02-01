import os
from zen_knit.data_types import Chunk, ChunkOption, ExecuatedChucnkOut, ParseData, ExecuatedChunk, ExecutedData
from ipykernel.inprocess import InProcessKernelManager
from jupyter_client import KernelManager, BlockingKernelClient
from queue import Empty
from nbformat.v4 import output_from_msg
import re
import joblib

database_query = """
from sqlalchemy import create_engine 
import pandas as pd 
engine = create_engine('{my_connection}')
with engine.begin() as con:
    {var_name} = pd.read_sql('{query}', con )
{var_name}.{result_in} """

class BaseExecutor(object):
    
    def __init__(self, data: ParseData):
        self.new_line_regex = re.compile("^\S*")
        self.data = data
        self.excuted_data = ExecutedData(global_options=data.global_options, chunks=[])
        self.cached_data = None
        self.load_cache()
        self._set_up_kernal()
        if self.data.global_options.input.matplot:
            self._preload_matplot()
        self._run_chucks()
        self._close_kernal()

    def _save_chunks(self):
        data = self.excuted_data
        file_name = self.data.global_options.input.file_name.split(".")[0]
        cache_file = self.data.global_options.output.dir +"/" +file_name + "._cache_data.jolib"
        joblib.dump(data, cache_file)

        
    def load_cache(self):
        if self.data.global_options.cache:
            file_name = self.data.global_options.input.file_name.split(".")[0]
            cache_file = self.data.global_options.output.dir +"/" + file_name + "._cache_data.jolib"
            try:
                self.cached_data = joblib.load(cache_file)
            except:
                pass

    def _set_up_kernal(self):
        global_options = self.data.global_options
        self.km = InProcessKernelManager(kernel_name=global_options.kernal)
        log_level = global_options.log_level
        if log_level != 'notset':
            log_file =  os.path.join(global_options.input.dir, "log.txt")
            f = open(log_file, "w")
        else:
            f = open(os.devnull, 'w')
        self.km.start_kernel(cwd=global_options.input.dir, stderr=f)

        self.kc = self.km.client()
        self.kc.start_channels()
        try:
            _ = self.kc.wait_for_ready()
        except RuntimeError:
            print("Timeout from starting kernel\nTry restarting python session and running it again")
            self._close_kernal()
            raise

        self.kc.allow_stdin = False

    def _close_kernal(self):
        self.kc.stop_channels()
        self.km.shutdown_kernel()

  
    def _run_chucks(self):
        for index, chunk in enumerate(self.data.chunks):
            if chunk.options.name:
                print(f"executing {chunk.options.name}")
            else:
                print(f"executing index {index}")
            self._run_chunck(chunk, index)
        self._save_chunks()

    def _run_and_save(self, code:str,  ec:ExecuatedChunk, type_:str):
        ran_code = self._run_code(code)
        if ran_code is not None:
            for r in ran_code:
                eco = ExecuatedChucnkOut(
                    output_type=type_,
                    data= r
                )
                ec.results.append(eco)

    def _run_sql(self, chunk:Chunk, ec:ExecuatedChunk):
        query = chunk.string_.replace("\n", " ")
        con_string =  chunk.options.con_string
        my_connection = os.getenv(con_string)
        
        var_name = chunk.options.name or "zen"
        if self.data.global_options.output.format == "pdf":
            result_in = "to_latex()"
        else:
            result_in = "to_html()"
        code = database_query.format(my_connection=my_connection, query=query, var_name=var_name, result_in=result_in)
        self._run_and_save(code, ec, "code")

    def _run_code_chunk(self, chunk:Chunk, ec:ExecuatedChunk):
        code = ""
        for partial_string in chunk.string_.splitlines():
            if self.new_line_regex.search(partial_string, 1):
                if code != "":
                    self._run_and_save(code, ec, chunk.type)
                    code = ""
                code = partial_string
            else:
                code = code + "\n" + partial_string
        
        self._run_and_save(code, ec, chunk.type)
    
    def _run_chunck(self, chunk:Chunk, index):
        if (self.data.global_options.cache) and (self.cached_data):
            if chunk.type == "code":
                if chunk.options.name:
                    print(f"cache {chunk.options.name}")
                else:
                    print(f"cache index {index}")
                    ec = self.cached_data.chunks[index]
                    self.excuted_data.chunks.append(ec)    
                    return
                
        self._pre_run(chunk)
        ec = ExecuatedChunk(chunk=chunk, results=[])

        if chunk.options.echo:
            eco = ExecuatedChucnkOut(
                output_type=chunk.type,
                data= {'code_text_raw': chunk.string_}
            )
            ec.results.append(eco)

        if (chunk.options.run) & (chunk.type == "sql"):
            self._run_sql(chunk, ec)

        if (chunk.options.run) & (chunk.type == "code"):
            self._run_code_chunk(chunk, ec)
        
        self.excuted_data.chunks.append(ec)    
        
    def _run_code(self, code):
        msg_id = self._send_to_kernal(code)
        return self._pull_data_from_kernal(msg_id)

    def _preload_matplot(self):
        init_matplotlib = """
            %matplotlib inline
            from IPython.display import set_matplotlib_formats
            set_matplotlib_formats('png', 'pdf', 'svg')
            import matplotlib
            """
        self._run_code(init_matplotlib)

    def _pre_run(self, chunk:Chunk):
        options = chunk.options
        if options.fig:
            fig_size = "matplotlib.rcParams.update({'figure.figsize' : ({height}, {width})})".foramt(height=options.fig_size[0], width=options.fig_size[1])
            f_dpi = "matplotlib.rcParams.update({'figure.dpi' : {dpi}})".format(dpi=options.fig_dpi)
            code = fig_size + "\n" + f_dpi
            self._run_code(code)

    def _send_to_kernal(self, code):
        msg_id = self.kc.execute(code, store_history=False)
        while True:
            try:
                msg = self.kc.get_shell_msg(timeout=10)
            except Empty:
                pass
            if msg['parent_header'].get('msg_id') == msg_id:
                break
            else:
                # not our reply
                continue
        return msg_id
    

    def _pull_data_from_kernal(self, msg_id):
        outs = []
        while True:
            try:
                msg = self.kc.iopub_channel.get_msg(block=True, timeout=4)
            except Empty:
                raise RuntimeError("Timeout waiting for IOPub output")

            if msg['parent_header'].get('msg_id') != msg_id and msg['msg_type'] != "stream":
                continue

            msg_type = msg['msg_type']
            content = msg['content']


            if msg_type == 'status':
                if content['execution_state'] == 'idle':
                    break
                else:
                    continue
            elif msg_type == 'execute_input':
                continue
            elif msg_type == 'clear_output':
                self.excuted_data.chunks = []
                continue
            elif msg_type.startswith('comm'):
                continue

            try:
                out = output_from_msg(msg)
            except ValueError:
                print("unhandled iopub msg: " + msg_type)
            else:
                outs.append(out)
        return outs
