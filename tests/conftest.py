import json
import logging
from pathlib import Path

import pandas as pd
import pytest

import plotly
import plotlyink
from plotly.utils import PlotlyJSONEncoder
from plotlyink.testing import assert_figure_equal

logger = logging.getLogger(__file__)

plotlyink.register_pandas_iplot_accessor()

DATA_DIR = Path(__file__).parent / 'data'
DATASETS_DIR = DATA_DIR / 'datasets'
FIGURE_DIR = DATA_DIR / 'figures'


# Add cmdline arguments
def pytest_addoption(parser):
    parser.addoption(
        "--regenerate-samples",
        action="store_true",
        default=False,
        help="Ask to regenerate samples")
    parser.addoption(
        "--generate-samples",
        action="store_true",
        default=False,
        help="Ask to generate samples for non existing ones only.")


class RecoderBase():
    def __init__(self, dataset, bucket_name, mode=None):
        self.mode = mode
        self.bucket_name = bucket_name
        self.dataset = dataset

        self.read_and_process_csv()

    def read_and_process_csv(self):
        self.df = pd.read_csv(DATASETS_DIR / '{}.csv'.format(self.dataset))

    def send_figure(self, fig):

        fig_path = FIGURE_DIR / '{}.json'.format(self.bucket_name)

        def compare_figure():
            fig_expected = json.load(open(fig_path.as_posix()))
            # As no PlotlyJSONDecoder:
            assert_figure_equal(
                json.loads(json.dumps(fig_expected, cls=PlotlyJSONEncoder)),
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            )

        def dump_figure():
            logger.info("Dumping figure into {}".format(fig_path))
            f = open(fig_path.as_posix(), 'w+')
            json.dump(fig, f, cls=plotly.utils.PlotlyJSONEncoder)

        if not self.mode:
            compare_figure()
        elif self.mode == 'regenerate':
            dump_figure()
        elif self.mode == 'generate':
            if fig_path.exists():
                compare_figure()
            else:
                dump_figure()
        else:
            raise NotImplementedError("mode: ", self.mode)


@pytest.fixture
def pokemon_recorder(request):
    mode = None  # test existing cassettes

    # generate samples and cassettes for new tests
    if request.config.getoption("--generate-samples"):
        mode = 'generate'

    # regenerate samples and cassettes for all tests
    if request.config.getoption("--regenerate-samples"):
        mode = 'regenerate'

    class Recorder(RecoderBase):
        def __init__(self, bucket_name):
            super().__init__('pokemon', bucket_name, mode)

        def read_and_process_csv(self):
            fpath = DATASETS_DIR / '{}.csv'.format(self.dataset)
            self.df = pd.read_csv(fpath).drop(
                columns=['#', 'Type 1', 'Type 2', 'Legendary']
            ).set_index('Name')

    yield Recorder
