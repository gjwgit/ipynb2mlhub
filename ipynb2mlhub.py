# -*- coding: utf-8 -*-

# Copyright (c) Togaware. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com

import argparse
import json
import sys

from markdown import markdown
from IPython.display import Markdown, display
from subprocess import Popen, PIPE, STDOUT

def typeset(c, lang):
    msg = ""
    for s in c['source']:
        p = Popen(['pandoc', '-f', 'markdown', '-t', 'plain'],
                  stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        msg += (p.communicate(input=memoryview(str.encode(s)))[0]).decode("utf-8")
    return('mlcat("", """' + msg + '""")\nmlask()\n')

def extract(c, lang):
    script = ""
    for src in c['source']:
        # Ignore lines that start with %
        ign = src.lstrip()
        if len(ign) > 0:
            ign = ign[0]
        else:
            ign = ""
        if ign == '%': continue
        # Ignore lines containing __future__
        if "__future__" in src: continue
        # Otherwise add in
        script += src
    return('mlcat("", """\n' + script + '\n""")\nmlask()\n' + script)

f = open(sys.argv[1]) # Need proper argparse handling.
nb = json.load(f)

lang = nb['metadata']['kernelspec']['language']
cells = nb['cells']

demo = "from IPython.display import display\n"

for c in cells:
    if c['cell_type'] == 'markdown':
        demo += "\n" + typeset(c, lang)
    elif c['cell_type'] == 'code':
        demo += "\n" + extract(c, lang)

print("from mlhub.pkg import azkey, azrequest, mlask, mlcat\n" + demo)

    
# Now iterate through the JSON cells and for each generate either code to display the text or the actual code to run.
