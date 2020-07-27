from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'deform',
    "python-dateutil",
    'pyramid',
    "pyramid_jwt",
    'pyramid_chameleon',
    "pyramid_openapi3",
    'waitress',
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'pyramid_tm',
    'sqlalchemy',
    'webtest',
    'zope.sqlalchemy'
]


setup(
    name='bp_app',
    install_requires=requires,
    extras_require={
        'development': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = bp_app:main'
        ],
        'console_scripts': [
            'initialize_bp_app_db = bp_app.initialize_db:main'
        ],
    },
)