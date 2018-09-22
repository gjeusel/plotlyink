import numpy as np
import plotly.graph_objs as go

from .colors import cl, to_rgba
from .utils import figure_handler, kwargshandler


class BasePlotMethods:
    """
    Base class for assembling a pandas plot using plotly.

    Args:
        data (pd.DataFrame):
    """

    @property
    def _kind(self):
        """Specify kind str. Must be overridden in child class"""
        raise NotImplementedError

    def __init__(self, data):
        self._data = data

    @staticmethod
    def _figure_handler(*args, **kwargs):
        return figure_handler(*args, **kwargs)

    def _get_traces(self, **kwargs):
        raise NotImplementedError

    def _get_figure(self, layout={}, **kwargs):
        return {'data': self._get_traces(**kwargs), 'layout': layout}

    def __call__(self, as_figure=False, as_image=False, as_url=False,
                 **kwargs):
        fig = self._get_figure(**kwargs)
        return self._figure_handler(
            fig=fig, as_figure=as_figure, as_image=as_image, as_url=as_url)


class ScatterPlot(BasePlotMethods):
    _kind = "scatter"

    def _get_traces(self, mode="lines", fill=False, **kwargs):
        """
        Args:
            mode (str): within ['lines', 'markers', 'area']
            fill (bool): has effect only for mode == 'lines'
        """
        x = self._data.index.tolist()
        y = self._data.columns.tolist()

        colors = kwargshandler.colors(self._data, **kwargs)
        kwargs_scatter = kwargshandler.scatter(**kwargs)
        traces = []

        for col in y:
            t = go.Scatter(x=x, y=self._data[col].values.tolist(), name=col)
            t["marker"]["color"] = colors[col]

            if mode == "lines":
                t.update({"mode": "lines"})
                if fill:
                    t.update({
                        "fill": "tozeroy",
                        "fillcolor": to_rgba(colors[col], 0.3)
                    })

            elif mode == "area":
                t.update({
                    "mode": "lines",
                    "fill": "tonexty",
                    "fillcolor": to_rgba(colors[col], 0.3),
                })

            elif mode == "markers":
                t.update({"mode": "markers", "marker": {"size": 10}})

            t.update(kwargs_scatter)
            traces.append(t)

        return traces

    def lines(self, fill=False, **kwargs):
        return self(mode="lines", fill=fill, **kwargs)

    def area(self, **kwargs):
        return self(mode="area", **kwargs)

    def markers(self, **kwargs):
        return self(mode="markers", **kwargs)


class BarPLot(BasePlotMethods):
    _kind = "bar"

    def _get_traces(self, mode="vertical", **kwargs):
        """
        Args:
            mode (str): within ['vertical', 'horizontal'].
        """
        x = self._data.index.tolist()
        y = self._data.columns.tolist()

        colors = kwargshandler.colors(self._data, **kwargs)
        traces = []

        for col in y:
            t = go.Bar(x=x, y=self._data[col].values.tolist(), name=col)
            t["marker"]["color"] = colors[col]

            if mode.lower() in ["horizontal", "h"]:
                t["orientation"] = "h"

            traces.append(t)

        return traces

    def bar(self, **kwargs):
        return self(mode="vertical", **kwargs)

    def hbar(self, **kwargs):
        return self(mode="horizontal", **kwargs)


class HeatMap(BasePlotMethods):
    _kind = "heatmap"

    def _get_traces(self, zmin=None, zmax=None, **kwargs):
        """"""
        x = self._data.index.tolist()
        y = self._data.columns.tolist()
        z = self._data.values.transpose().tolist()

        # values min & max:
        zmin = zmin if zmin else z[~np.isnan(z)].min()
        zmax = zmax if zmax else z[~np.isnan(z)].max()

        # Colors handle for heatmap a little bit different.
        colors = kwargshandler.colors(self._data, **kwargs)
        colorscale = []
        for i, key in enumerate(colors):
            colorscale.append([float(i) / len(colors), colors[key]])

        # Greys, YlGnBu, Greens, YlOrRd, Bluered, RdBu, Reds, Blues, Picnic,
        # Rainbow, Portland, Jet, Hot, Blackbody, Earth, Electric, Viridis, Cividis

        heatmap = go.Heatmap(
            x=x,
            y=y,
            z=z,
            zmin=zmin,
            zmax=zmax,
            colorscale=colorscale,
        )

        heatmap.update(kwargshandler.heatmap(**kwargs))
        return [heatmap]


class TablePlot(BasePlotMethods):
    _kind = "table"

    def _get_traces(self, with_index=True, color=cl.red_lighter, **kwargs):
        df = self._data
        if with_index:
            df = df.reset_index()

        row_c1 = cl.white
        row_c2 = to_rgba(color, 0.2)
        row_colors = []
        for i in range(0, df.shape[0] - 1, 2):
            row_colors.append(row_c1)
            row_colors.append(row_c2)

        header_values = ["<b>{}</b>".format(c) for c in df.columns]
        cells_values = df.round(3).values.transpose().tolist()

        header = {"values": header_values, "fill": {"color": color}}
        cells = {"values": cells_values, "fill": {"color": [row_colors]}}

        table = go.Table(header=header, cells=cells, **kwargs)
        table.update(kwargshandler.table(**kwargs))
        return [table]


class BoxPlot(BasePlotMethods):
    _kind = "box"

    def _get_traces(self, normalize=False, **kwargs):
        df = self._data

        if normalize:
            for col in df.columns:
                serie = df[col].dropna()
                # df[col] = (serie - serie.mean()) / serie.std()
                df[col] = (serie - serie.min()) / (serie.max() - serie.min())

        # x = self._data.index
        y = self._data.columns.tolist()

        colors = kwargshandler.colors(self._data, **kwargs)
        kwargs_box = kwargshandler.box(**kwargs)
        traces = []

        for col in y:
            t = go.Box(y=df[col].dropna(), name=col)
            t["marker"]["color"] = colors[col]

            t.update(kwargs_box)
            traces.append(t)

        return traces
