import os
import sys
from pathlib import Path

# Добавляем путь к проекту
project_root = Path(__file__).parents[2]
sys.path.insert(0, str(project_root))

project = 'Password Generator'
copyright = '2025, alex'
author = 'alex'

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
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'show-inheritance': True,
}
autoclass_content = 'both'

# Настройки для Napoleon (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# Язык
language = 'ru'

# Автоматическое документирование всех членов классов
autodoc_default_flags = ['members', 'undoc-members', 'private-members', 'special-members', 'inherited-members', 'show-inheritance']
