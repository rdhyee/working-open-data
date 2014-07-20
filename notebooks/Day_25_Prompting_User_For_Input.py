# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# code that might be executing with `IPython.notebook.kernel.execute`: https://github.com/ipython/ipython/blob/3c2f44d25fbed7a76ea15988b195439b9ccac288/IPython/frontend/html/notebook/static/services/kernels/js/kernel.js#L291
# 
# A great elaboration on 2-way communication between Python and JavaScript in the notebook: http://jakevdp.github.io/blog/2013/06/01/ipython-notebook-javascript-python-communication/

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

