import plotly
from .config import set_config_file, get_config_file, run_from_ipython
from .register_pandas_accessors import FrameIplotMethods


# If inside ipython shell, init_notebook_mode
# connected = True -> for smaller file sizes (plotly.js will be loaded from an
# online CDN inplace of inlining the entire plotly.js into the notebook)
if run_from_ipython():
    plotly.offline.init_notebook_mode(connected=False)
