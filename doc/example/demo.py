import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from zen_knit.formattor import get_formatter
from zen_knit.formattor.html_formatter import HTMLFormatter
from zen_knit.data_types import ChunkOption, OrganizedData, GlobalOption, OrganizedChunk, OrganizedChuckType, Input, Output, latexOuput, htmlOutput
from datetime import datetime

t = OrganizedChuckType

g = GlobalOption(
    title = "python example",
    author = "Dr P B Pael",
    date = 'CURRENT_DATE',
    input= Input(
        matplotlib = True,
    ),
    output = Output(
        fig_dir = "figures",
        format = "html",
        file_name= "html_python.html",
        dir = "output",
        html = htmlOutput(
        )
    )
    
)

contents = []

# type: str
# str_data: str = ""
# complex_data: dict = {}

contents.append(OrganizedChunk(type=t.Markdown.value, str_data="## with class"))

my_string = """
class test:
    def __init__(self):
        print("hi")
        return "hi"
    
    def test(self):
        print("hi")
        return "hi"
t = test()
t.test()
"""
contents.append(OrganizedChunk(type=t.Code.value, str_data=my_string))


my_string = """
import numpy as np
import matplotlib.pyplot as plt
"""
contents.append(OrganizedChunk(type=t.Code.value, str_data=my_string))

my_string = """
# Lax example
$$ \\begin{pmatrix}
x^2 + y^2 &= 1 \\\\
y &= \sqrt{1 - x^2}
\end{pmatrix}$$
"""
contents.append(OrganizedChunk(type=t.Markdown.value, str_data=my_string))

my_string = """
xpoints = np.array([1, 8])
ypoints = np.array([3, 10])
"""
contents.append(OrganizedChunk(type=t.Code.value, str_data=my_string))

xpoints = np.array([1, 8])
ypoints = np.array([3, 10])
plt.plot(xpoints, ypoints, 'o')
file_name = "output/figures/books_read.png"
plt.savefig(file_name)
chunk_option = ChunkOption(
    render = True,
    fig =  True,
    fig_size =  (6, 4),
    fig_dpi = 200,
)
contents.append(OrganizedChunk(type=t.Plot.value, complex_data={"plots": [file_name], "options": chunk_option }))


d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
my_string = df.to_html()

contents.append(OrganizedChunk(type=t.Table.value, str_data=my_string))

og = OrganizedData(
    global_options=g,
    chunks = contents
)
f = get_formatter(g.output.format)
 # or its derivative class
bf = f(og)
bf.run()