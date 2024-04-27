import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'iPre: Calendarizacion Interrogaciones Escuela Ingeniería'
copyright = '2023, Gustavo Angulo y Francisco Solís'
author = 'Gustavo Angulo y Francisco Solís'
release = '2023'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.todo']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
