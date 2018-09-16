from setuptools import setup

try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    BuildDoc = None

setup(
    package_dir={'': 'src'},
    setup_requires=['pbr'],
    pbr=True,
    cmdclass={'build_sphinx': BuildDoc},
)
