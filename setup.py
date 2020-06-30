from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'waitress',
]

setup(
    name='bp_app',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = bp_app:main'
        ],
    },
)