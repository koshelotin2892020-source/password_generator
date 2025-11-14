import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

project = 'Password Generator'
copyright = '2024, Александр'
author = 'Александр'

release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Настройки для autodoc
autodoc_member_order = 'groupwise'
autodoc_default_flags = ['members', 'undoc-members']
autoclass_content = 'both'

# Настройки для Napoleon (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# Язык
language = 'ru'
