def test_scatter_line_pokemon(pokemon_recorder):
    r = pokemon_recorder('pokemon_scatter_noargs')
    fig = r.df.iplot.scatter()
    r.send_figure(fig)
