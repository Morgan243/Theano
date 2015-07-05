"""Extends printing module by dynamic visualizations."""

# Authors: Christof Angermueller <cangermueller@gmail.com>

import os.path

from theano.printing import pydotprint
from formatting import GraphFormatter



def replace_patterns(x, replace):
    """ Replaces patterns defined by `replace` in x."""
    for from_, to in replace.items():
        x = x.replace(str(from_), str(to))
    return x


def d3dot(fct, node_colors=None, *args, **kwargs):
    if node_colors is None:
        node_colors = {'input': 'limegreen',
                       'output': 'dodgerblue',
                       'unused': 'lightgrey'
                       }

    dot_graph = pydotprint(fct, format='dot', return_image=True,
                           node_colors=node_colors, *args, **kwargs)
    dot_graph = dot_graph.replace('\n', ' ')
    dot_graph = dot_graph.replace('node [label="\N"];', '')
    return dot_graph


def d3write(fct, path, *args, **kwargs):
    # Convert theano graph to pydot graph and write to file
    gf = GraphFormatter(*args, **kwargs)
    g = gf.to_pydot(fct)
    g.write_dot(path)


def d3print(fct, outfile=None, return_html=False, print_message=True,
            *args, **kwargs):
    """Creates dynamic graph visualization using d3.js javascript library.

    :param fct: A compiled Theano function, variable, apply or a list of
                variables
    :param outfile: The output file
    :param return_html: If True, return HTML code
    :param print_message: If True, print message at the end
    :param *args, **kwargs: Parameters passed to pydotprint
    """

    # Create dot file
    dot_file = os.path.splitext(outfile)[0] + '.dot'
    d3write(fct, dot_file, *args, **kwargs)


    # Read template HTML file and replace variables
    template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 'template.html')
    f = open(template_file)
    template = f.read()
    f.close()
    replace = {
        '%% DOT_FILE %%': dot_file,
    }
    html = replace_patterns(template, replace)

    # Write output file
    if outfile is not None:
        f = open(outfile, 'w')
        f.write(html)
        f.close()
        if print_message:
            print('The output file is available at %s' % (outfile))

    if return_html:
        return html
