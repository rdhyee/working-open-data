# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# https://plus.google.com/115875830338788300419/posts/cJFqX2Rpvzn

import IPython.core.display

def ipynb_input(varname, prompt=''):
    """Prompt user for input and assign string val to given variable name."""
    js_code = ("""
        var value = prompt("{prompt}","");
        var py_code = "{varname} = '" + value + "'";
        IPython.notebook.kernel.execute(py_code);
    """).format(prompt=prompt, varname=varname)
    return IPython.core.display.Javascript(js_code)

# <codecell>

ipynb_input("name", prompt='Enter your name: ')

# <codecell>

print name

# <codecell>


