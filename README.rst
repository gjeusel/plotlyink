===============================
plotlyink
===============================

.. image:: https://travis-ci.org/gjeusel/plotlyink.svg?branch=master
    :target: https://travis-ci.org/gjeusel/plotlyink
.. image:: https://readthedocs.org/projects/plotlyink/badge/?version=latest
   :target: http://plotlyink.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://codecov.io/gh/gjeusel/plotlyink/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/gjeusel/plotlyink
.. image:: https://badge.fury.io/py/plotlyink.svg
   :target: https://pypi.python.org/pypi/plotlyink/
   :alt: Pypi package


Marying plotly & pandas

:License: MIT license
:Documentation: http://plotlyink.readthedocs.io/en/latest
:Source: https://github.com/gjeusel/plotlyink


Installation
------------
.. code:: bash

    pip3 install plotlyink


Overview
--------
.. code:: python

    import pandas as pd
    import plotlyink
    df = pd.DataFrame({
        'one' : [1., 2., 3., 4.],
        'two' : [4., 3., 2., 1.],
        })

    # open .html in your browser:
    df.iplot.scatter()

    # get figure:
    fig = df.iplot.scatter(as_figure=True)


For more, see: `Tutorial Notebook <http://nbviewer.jupyter.org/github/gjeusel/plotlyink/blob/master/notebooks/tutorial.ipynb>`_.
