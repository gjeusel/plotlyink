import pytest
from plotlyink import colors


@pytest.mark.parametrize('scale', [
    {'scale': 'spectral', 'ncolors': 11, 'expected': ['rgb(158,1,66)', 'rgb(213,62,79)', 'rgb(244,109,67)', 'rgb(253,174,97)', 'rgb(171,221,164)', 'rgb(102,194,165)', 'rgb(50,136,189)', 'rgb(94,79,162)']},
    {'scale': 'spectral', 'ncolors': 10, 'expected': ['rgb(158,1,66)', 'rgb(213,62,79)', 'rgb(244,109,67)', 'rgb(253,174,97)', 'rgb(171,221,164)', 'rgb(102,194,165)', 'rgb(50,136,189)', 'rgb(94,79,162)']},
])
def test_filter_on_brightness(scale, brightness_thresh=220):
    expected = scale.pop('expected')
    scale = colors.find_scale(**scale)
    ret = colors.filter_on_brightness(scale, brightness_thresh=brightness_thresh)
    assert expected == ret
