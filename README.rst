About Zen-Knit:
---------------

Zen-Knit is a formal (PDF), informal (HTML) report generator for data analyst and data scientist who wants to use python. Inspired from Pweave. 
Zen-Knit is good for creating reports, tutorials with embedded python

Features:
---------

* Python 3.6+ compatibility
* Support for IPython magics and rich output.
* **Execute python code** in the chunks and **capture** input and output to a report.
* **Use hidden code chunks,** i.e. code is executed, but not printed in the output file.
* Capture matplotlib graphics.
* Evaluate inline code in documentation chunks marked using ```{ }`` 
* Publish reports from Python scripts. Similar to R markdown.
* integrate it in your process. It will fit your need rather than you need to adjust for tool.

Install
-----------------------

From PyPi::

  pip install --upgrade zen-knit

or download the source and run::

  python setup.py install



License information
-------------------

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


How to Use it
-------------

  pip install zen-knit

  knit -f doc/example/html_example.pyz  -ofd doc/example/output/
  
  knit -f doc/example/pdf_example.pyz  -ofd doc/example/output/