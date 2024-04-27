# iPre: Calendarización Interrogaciones

## Descargar repositorio

Para poder descargar este repositorio, se recomienda clonarlo. Para esto utilizar:

```sh
git clone https://github.com/panchouc/iPre.git
```
en algún directorio de interés.

## Instalación librerías

Para instalar las librerías necesarias, se debe ejecutar el siguiente comando desde el directorio donde haya clonado este repositorio:

```sh
pip install -r requirements.txt
```

En caso de tener algún problema, la versión de las librerías que tengo yo son:

- pandas: 1.5.3
- numpy: 1.23.5
- networkx: 3.0
- matplotlib: 3.7.1
- openpyxl: 3.1.2
- pytest: 7.3.1
- bokeh: 2.4.3
- polars: 0.16.16


## Ejecución


Para ejecutar el proyecto, cerciorarse de estar en el directorio `src`. Luego de esto, correr el archivo `main.py`

### Flujo del programa
A continuación se listan todos los pasos e instrucciones que son ejectuadas en el procesamiento de los datos y creación de los grafos en el archivo `main.py`.

#### Grafo de prerrequisitos

1) Se utiliza la función `cursos_ingenieria_polars`, la cual está encargada de obtener únicamente los cursos que pertenecen a la Facultad de Ingeniería y se eliminan los cursos que no tienen prerrequisitos asociados.
2) Se utiliza la función `diccionario_cursos_y_prerrequisitos`, la cual utiliza la forma conjuntiva normal para extraer cuales son los verdaderos prerrequisitos. Por ejemplo, si se tiene que los requisitos de un curso cualquiera son: A y B ó B y C, en realidad, el único prerrequisito es B. Si tiene como prerrequisitos los cursos
A y B ó C y D, en realidad, no tiene ningún prerrequisito. Lo que se obtiene como resultado es un diccionario donde las keys son las siglas y el valor asociado son los prerrequisitos.
3) Se crea un grafo dirigido a partir del diccionario entregado anteriormente y se invierten los arcos. Esto, para que los arcos queden de la forma: Prerrequisito -> Curso.
4) Se aplica una la función `anadir_arcos_transitividad`. Estos arcos se pueden pensar en que cumplen una cierta propiedad de transitividad. Por ejemplo, si se tienen los nodos y arcos tales que: A -> B -> C -> D, lo que hace esta función (o lo que debería de hacer), es que añade un arco A -> C, A -> D y B -> D. No se pueden añadir los arcos C -> A y D -> A por ejemplo. Solo se pueden añadir arcos desde nodos que van desde la izquierda a la derecha y en un orden creciente de aparición.  
5) Luego se utiliza la función `nuevos_arcos` que retorna un diccionario de donde cada key corresponde a la sigla-sección y el valor asociado es una lista de todos sus vecinos en el grafo que quedó luego de aplicar el paso 4).

#### Grafo de módulos

1) Se utiliza la función `cursos_y_horario_polars` la cual retorna un dataframe donde solamente contiene los horarios correspondientes a las cátedras.
2) Se utiliza la función `cursos_con_macroseccion`.
3) Se utiliza la función `grafo_mismo_modulo`
4) Se utiliza la función `reemplazar_siglas_con_macrosecciones`

#### Flujo típico

Lo que uno haría normalmente es ejecutar el código en el siguiente orden


- Revisar el parámetro `NUM_EXPERIMENTO`
- `main.py`
- `optimization.py`
- `out_calendarios.py`
- `test.py` (Opcional)
- `out_resultados_excel.py` (Genera archivo `.csv` para utilizar como input en el programa de salas)

## Ejemplos

En `src` se encuentra el archivo `grafo.ipynb` donde se puede ver un grafo de los cursos con sus respectivos requisitos.

## Documentación

Para tener la documentación más vigente del código, ejecutar el siguiente comando desde el directorio `docs`:

```sh
MINGW32-make html
```

### Building documentation from source

En caso de no estar seguro de tener la última documentación, borrar la carpeta docs y realizar los siguientes pasos.
Abrir una cmd y ejecutar el siguiente comando desde el directorio `src`


```sh
mkdir docs
cd docs
```

Luego hacer
```sh
sphinx-quickstart
```

Luego, es necesario poner el siguiente código en el archivo `conf.py`

```python
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
```

Luego, es necesario ejecutar

```sh
sphinx-apidoc -o . ..
```

Y finalmente para generar el output poner

```sh
MINGW32-make html
```


# Integrantes
- Gustavo Angulo
- Francisco Solís