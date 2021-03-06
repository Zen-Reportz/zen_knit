#---
# title: Zen Markdown Demo
# author: Dr. P. B. Patel
# date: CURRENT_DATE
# output: 
#     format: pdf
#     latex: 
#         header: \usepackage{booktabs}
#         geometry_parameters: text={20cm,20cm},centering
#---

## with class 
# %%{run=true, echo=true}
class test:
    def __init__(self):
        print("hi")
    
    def test(self):
        print("hi")

t = test()
t.test()

#```


# %%{run=true, echo=true, render=false}
import numpy as np
import matplotlib.pyplot as plt
#```

## Lax example

# $$ \begin{pmatrix}
# x^2 + y^2 &= 1 \\
# y &= \sqrt{1 - x^2}
# \end{pmatrix}$$


# %%{run=true, echo=true, render=true}
import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([1, 8])
ypoints = np.array([3, 10])
print(xpoints)
print(ypoints)
#```



## Matplot lib example
# %%{run=true, echo=true, render=true}

plt.plot(xpoints, ypoints, 'o')
#```


# %%{run=true, echo=true, render=true}
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
df.to_markdown()
#```


# %%{run=true, echo=true, render=true}
import pandas as pd
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
df.to_latex()
#```

