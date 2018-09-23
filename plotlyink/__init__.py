from pathlib import Path

import plotly

from .config import get_config_file, run_from_ipython, set_config_file

PKG_DIR = Path(__file__).parents[1]
SRC_DIR = PKG_DIR / 'plotlyink'
NOTEBOOKS_DIR = PKG_DIR / 'notebooks'

# If inside ipython shell, init_notebook_mode
# connected = True -> for smaller file sizes (plotly.js will be loaded from an
# online CDN inplace of inlining the entire plotly.js into the notebook)
if run_from_ipython():
    plotly.offline.init_notebook_mode(connected=False)


def register_pandas_iplot_accessor():
    from .register_pandas_accessors import FrameIplotMethods
