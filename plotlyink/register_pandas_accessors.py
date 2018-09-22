import pandas as pd

from .core import BarPLot, HeatMap, ScatterPlot, TablePlot, BoxPlot
from .finegrained import get_fine_grained_figure
from .utils import recursive_update


@pd.api.extensions.register_dataframe_accessor("iplot")
class FrameIplotMethods():
    """DataFrame interactive plotting accessor and method

    Examples
    --------
    >>> df.iplot.scatter.line()
    >>> df.iplot.scatter.line(fill=True)
    >>> df.iplot.scatter.area()

    These plotting methods can also be accessed by calling the accessor as a
    method with the ``kind`` argument:
    ``df.plot(kind='line')`` is equivalent to ``df.plot.line()``
    """

    def __init__(self, data):
        self._data = data

        # Scatter plots:
        self.scatter = ScatterPlot(data)

        # Bar plots:
        self._bar = BarPLot(data)
        self.bar = self._bar.bar
        self.hbar = self._bar.hbar

        # Heatmap plots:
        self.heatmap = HeatMap(data)

        # Table:
        self.table = TablePlot(data)

        # Box:
        self.box = BoxPlot(data)

    def __call__(self, x=None, y=None, kind='scatter', mode='lines', **kwargs):
        return self.__dict__[kind](x=x, y=y, mode=mode)

    def finegrained(self, path_specdf, layout={}, **kwargs):
        return get_fine_grained_figure(df=self._data, path_specdf=path_specdf,
                                       layout=layout, **kwargs)

    def missing_values(self, layout={}, **kwargs):
        """Get an overview of missing values."""
        df = self._data.isna().astype(int)
        kwargs.update(
            {'zmin': 0, 'zmax': 1,
             'colors': 'reds', 'ncolors': 9,
             'xgap': 3, 'ygap': 3,
             'showscale': False, }
        )

        layout = recursive_update(
            layout, updater={
                'xaxis': {'showgrid': False, 'zeroline': False},
                'yaxis': {'showgrid': False, 'zeroline': False},
            })
        return df.iplot.heatmap(layout=layout, **kwargs)

    def correlation_matrix(self, layout={}, **kwargs):
        """Plot the Correlation Matrix."""
        df = self._data.corr()
        kwargs.update({
            'zmin': -1, 'zmax': 1,
            'colors': 'rdbu', 'ncolors': 9,
            'xgap': 3, 'ygap': 3, 'dtick': 1,
            'colorbar': {'x': 1 - 0.22},
        })

        layout = recursive_update(
            layout, updater={
                'xaxis': {'showgrid': False, 'zeroline': False},
                'yaxis': {'showgrid': False, 'zeroline': False},
            })

        # square for 1920x1080 screens in awating for better plotly option
        layout = recursive_update(
            layout, updater={
                'yaxis': {'domain': [0, 1]},
                'xaxis': {'domain': [0.28215, 1 - 0.28215]},
            })

        return df.iplot.heatmap(layout=layout, **kwargs)
