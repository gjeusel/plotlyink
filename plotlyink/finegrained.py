import copy
from pathlib import Path
import pandas as pd
import collections
import colorlover
import plotly.graph_objs as go

from .utils import kwargshandler, figure_handler, recursive_update
from .colors import cl


def read_finegrained_refs(path):
    """Read fine grained reference csv file."""
    if isinstance(path, str):
        path = Path(path).absolute()
    elif isinstance(path, Path):
        path = path.absolute()
    else:
        raise TypeError('path of type {} no handled'.format(type(path)))

    df = pd.read_csv(path.as_posix())
    df = df.dropna(how='all', axis=0)  # treat void lines in csv that help the reading

    predefined_colors = [c for c in dir(cl) if not callable(c)]
    colors = []
    if 'marker.color' in df.columns.tolist():
        for i, row in df.iterrows():
            color = row['marker.color']
            if color in predefined_colors:
                colors.append(cl.__dict__[color])
            else:
                raise NotImplementedError(color)  # TODO

    df['marker.color'] = colors
    return df


def csv2dict(serie):
    """Convert line from reference csv into kwargs for plot.
    A dot in the column name of the reference means a separator for embed keys.

    Args:
        serie (pd.Series): row of the reference csv

    Returns: (dict)
    """
    dct = dict(serie)

    # Pop not needed keys for trace
    for e in ['column', 'plottype']:
        if e in dct.keys():
            dct.pop(e)

    result = copy.deepcopy(dct)
    # Recreate dict from keys with '.' in the name:
    for key in dct.keys():
        lst_keys = key.split('.')
        tree_dict = dct[key]
        for k in reversed(lst_keys):
            tree_dict = {k: tree_dict}
        result.pop(key)

        result = recursive_update(result, tree_dict)

    return result


def get_fine_grained_traces(df, path_specdf):
    """Return a list of traces with specification coming from a csv file.

    Args:
        df (pd.DataFrame): the dataframe to be plotted.
        path_spec (str or pathlib.Path): path to csv file containing specifications.

    Returns: a list of traces
    """

    # Some checks on the DataFrame to be plotted:
    if df.columns.duplicated().any():
        raise ValueError('Your Dataframe contains duplicated column names: '
                         '{}'.format(df.columns[df.columns.duplicated()]))

    specdf = read_finegrained_refs(path_specdf)

    traces = []
    for col in specdf['column']:
        spec = specdf[specdf['column'] == col].iloc[0].dropna()

        if col in df.columns:
            serie = df[col]
            x_values = serie.index.tolist()
            y_values = serie.tolist()

            kwargs = csv2dict(spec)

            plottype = spec['plottype']
            plottype = plottype[:1].upper() + plottype[1:].lower()

            traces.append(
                go.__dict__[plottype](
                    x=x_values,
                    y=y_values,
                    legendgroup=spec['name'],
                    **kwargs
                ))

    return traces


def get_fine_grained_figure(df, path_specdf, layout={},
                            as_figure=False, as_image=False, as_url=False):
    traces = get_fine_grained_traces(df=df, path_specdf=path_specdf)
    fig = {'data': traces, 'layout': layout}
    return figure_handler(fig=fig, as_figure=as_figure, as_image=as_image,
                          as_url=as_url)
