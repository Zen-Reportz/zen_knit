# Change Log

## [0.2.5]
- *py* file support
- moved cache into ouput object
## [0.2.1]
- *page_size* in latexOuput class

## [0.2.0]
- Input and Output Header Pyz (Zen Markdown / Python Markdown)
- header (latex_header) is now accepts multiline
- output moved to output.format
    
### Breaking change
some options moved from GlobalOption 
- *input_dir* moved to Input class, and renamed as **dir**
- *input_file_name* moved to Input class, and renamed as **file_name**
- *matplot* moved to Input class
- *fig_dir* moved to Output class
- *output_format* to Output class, and renamed as **format**
- *output_file_name* to Output class, renamed as **file_name**
- *output_dir* to Output class, and rename as **dir**
- *cache* to Output class
- *css* to move to htmlOutput
- *latex_header* to move to htmlOutput, renamed as **header**
- moved cache into ouput object


