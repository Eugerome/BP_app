from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'waitress',
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
]


setup(
    name='bp_app',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = bp_app:main'
        ],
    },
)