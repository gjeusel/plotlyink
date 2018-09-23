import logging
import subprocess

import nbformat as nbf

from plotlyink import NOTEBOOKS_DIR

from .conftest import FIGURE_DIR

logger = logging.getLogger(__name__)

git_label = subprocess.check_output(["git", "describe",
                                     "--always"]).strip().decode('utf-8')


def test_generate_summarize_html():
    nb = nbf.v4.new_notebook()
    cell_title = "# Tests Report Plotlyink {}".format(git_label)
    cell_imports = """
import plotlyink
plotlyink.register_pandas_iplot_accessor()

import plotly
plotly.offline.init_notebook_mode(connected=True)

import json
"""

    nb['cells'] = [
        nbf.v4.new_markdown_cell(cell_title),
        nbf.v4.new_code_cell(cell_imports),
    ]

    files = [p for p in FIGURE_DIR.iterdir()]

    for i, f in enumerate(files):
        cell = """
fig = json.load(open('{0}'))
fig['layout']['title'] = '{1}'
plotly.offline.iplot(fig)
""".format(f.as_posix(), f.stem)

        nb['cells'].append(nbf.v4.new_code_cell(cell))

    fout = NOTEBOOKS_DIR / 'summarize_{}.ipynb'.format(git_label)
    nbf.write(nb, fout.as_posix())
    logger.info('{} has been generated.'.format(fout))
