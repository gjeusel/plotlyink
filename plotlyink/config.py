def run_from_ipython():
    """Return boolean whether is running from ipython."""
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def run_from_jupyter():
    import os
    if 'bin/jupyter' in os.environ['_']:
        return True
    else:
        return False


def get_config_file():
    raise NotImplementedError


def set_config_file():
    raise NotImplementedError
