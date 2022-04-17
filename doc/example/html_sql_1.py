#---
#title: Zen Markdown Demo
#author: Dr. P. B. Patel
#date: CURRENT_DATE
#output: 
#    format: html
#    html: 
#        css: skleton
#---

## with sql
# %%{sql}
"""SELECT * 
FROM stocks"""
#```




# %%{run=true, echo=true, render=true}
zen.to_html()
#```

## with custom con string
# %%{sql, con_string=my_con_string, name=custom_df}
"""SELECT * 
FROM stocks"""
#```




# %%{run=true, echo=true, render=true}
custom_df.to_html()
#```