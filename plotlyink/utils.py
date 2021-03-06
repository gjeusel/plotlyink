from collections import Mapping, namedtuple

import plotly
import plotly.graph_objs as go

from .colors import to_plotly_colors_dict
from .config import run_from_ipython, run_from_jupyter


def filter_kwargs_on_list(kwargs, keys):
    """
    Simple function that construct a dictionnary with keys if is in kwargs.
    """
    out = {}
    for k in keys:
        if k in kwargs:
            out[k] = kwargs[k]

    return out


def retrieve_colors_kwargs(data, **kwargs):
    """Construct dict based on valid kwargs for colors."""
    colors_kwargs = filter_kwargs_on_list(
        kwargs, ["colors", "ncolors", "filter_brightness"]
    )
    return to_plotly_colors_dict(data.columns, **colors_kwargs)


def retrieve_scatter_kwargs(**kwargs):
    lst_keys_scatter = dir(go.Scatter())
    return filter_kwargs_on_list(kwargs, lst_keys_scatter)


def retrieve_heatmap_kwargs(**kwargs):
    lst_keys_heatmap = dir(go.Heatmap())
    return filter_kwargs_on_list(kwargs, lst_keys_heatmap)


def retrieve_table_kwargs(**kwargs):
    lst_keys_table = dir(go.Table())
    return filter_kwargs_on_list(kwargs, lst_keys_table)


def retrieve_box_kwargs(**kwargs):
    lst_keys_box = dir(go.Box())
    return filter_kwargs_on_list(kwargs, lst_keys_box)


KwargsOptions = namedtuple(
    "KwargsOptions", ["colors", "scatter", "heatmap", "table", "box"]
)

kwargshandler = KwargsOptions(
    colors=retrieve_colors_kwargs,
    scatter=retrieve_scatter_kwargs,
    heatmap=retrieve_heatmap_kwargs,
    table=retrieve_heatmap_kwargs,
    box=retrieve_box_kwargs,
)


def figure_handler(fig, as_figure, as_image, as_url):
    """Handle what to do with plotly fig."""
    if not any([as_figure, as_image, as_url]):
        if run_from_ipython():
            if run_from_jupyter():
                return plotly.offline.iplot(fig)
            else:
                return plotly.offline.plot(fig)
        else:
            return fig

    if as_figure:
        return fig
    elif as_image:
        raise NotImplementedError
    elif as_url:
        raise NotImplementedError


def recursive_update(result, updater):
    """Recursievly update a dictionnary by recreating it lowest embed.

    Example:
        dct = {'marker' = {'size': 12}
    Args:
<<<<<<< HEAD
        result (dict): the resulted dictionnary
        updater (dict): the input dictionnary
        """
    for key, value in updater.items():
        if isinstance(value, Mapping):
            result[key] = recursive_update(result.get(key, {}), value)
        else:
            result[key] = value
    return result
