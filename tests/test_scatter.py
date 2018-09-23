import json

from plotly.utils import PlotlyJSONEncoder
from plotlyink.colors import cl
from plotlyink.testing import assert_figure_equal


def test_pokemon_scatter_line(pokemon_recorder):
    r = pokemon_recorder('pokemon_scatter_lines_noargs')
    fig = r.df.iplot.scatter()

    # Verify if default params lead to same as lines method:
    assert_figure_equal(
        json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
        json.loads(
            json.dumps(r.df.iplot.scatter.lines(), cls=PlotlyJSONEncoder)),
    )

    r.send_figure(fig)


def test_pokemon_scatter_line_filled(pokemon_recorder):
    r = pokemon_recorder('pokemon_scatter_lines_fill')
    fig = r.df.iplot.scatter(fill=True)
    r.send_figure(fig)


def test_pokemon_scatter_area(pokemon_recorder):
    r = pokemon_recorder('pokemon_scatter_area_noargs')
    fig = r.df.iplot.scatter.area()
    r.send_figure(fig)


def test_pokemon_scatter_markers(pokemon_recorder):
    r = pokemon_recorder('pokemon_scatter_markers_noargs')
    fig = r.df.iplot.scatter.markers()
    r.send_figure(fig)


def test_pokemon_scatter_markers_size(pokemon_recorder):
    r = pokemon_recorder('pokemon_scatter_markers_size')
    fig = r.df.iplot.scatter.markers(marker={'size': 5})
    r.send_figure(fig)


def test_pokemon_scatter_markers_lots_of_args(pokemon_recorder):
    r = pokemon_recorder('pokemon_scatter_markers_lots_of_args')
    fig = r.df.iplot.scatter.markers(
        marker={'size': 5, 'symbol': 'diamond'}, opacity=0.8,
        hoverlabel={'bordercolor': cl.blue},
        showticklabels=False, tickwidth=2, ticklen=10, ticks="inside",
    )
    r.send_figure(fig)
