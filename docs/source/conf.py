# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sys
from pathlib import Path

PROJECT_ROOT = Path('.').resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT / 'src'))

# -- Project information -----------------------------------------------------

# import metanetx_sdk

project = 'MetaNetX SDK'
copyright = '2019, Moritz E. Beber'
author = 'Moritz E. Beber'

# The full version, including alpha/beta/rc tags
# release = metanetx_sdk.__version__


# -- General configuration ---------------------------------------------------

import sphinx_material

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx_material',
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for napoleon output ---------------------------------------------

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_material'
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'nav_title': project,
    'nav_links': [
        {'href': 'reference', 'title': 'API Reference', 'internal': True}
    ],
    'base_url': 'https://metanetx-sdk.readthedocs.io',
    'color_primary': 'teal',
    'color_accent': 'light-green',
    'repo_url': 'https://github.com/Midnighter/metanetx-sdk/',
    'repo_name': project,
    'globaltoc_depth': 2,
    'globaltoc_collapse': False,
    'globaltoc_includehidden': False,
}
