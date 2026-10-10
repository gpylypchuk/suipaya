# suipaya

Sitio personal de Geronimo Pylypchuk con resúmenes de cursos, en
[Suipaya](https://gpylypchuk.github.io/suipaya). Está hecho con Jekyll 4.3 y el
tema [tufte-jekyll](https://github.com/clayh53/tufte-jekyll) de Clay Harmon (licencia
MIT, ver `LICENSE`).

## Correr el sitio en local

Hace falta Ruby 3.2.2 (la versión está en `.ruby-version`, con rbenv se toma sola).

```sh
bundle install
bundle exec jekyll serve
```

El sitio queda en http://127.0.0.1:4000.

## Estructura

```
_cursos/cs149.md                    →  /cs149/
_clases/cs149/clase01.md            →  /cs149/clase01/
_assignments/cs149/assignment1.md   →  /cs149/assignment1/
```

Cada colección tiene su layout asignado en `_config.yml`, así que los archivos no
necesitan declarar `layout`.

## Agregar un curso

Crear `_cursos/<nombre>.md`. El nombre del archivo, sin extensión, es el identificador
del curso y su URL: `cs149.md` queda en `/cs149/`. Usar minúsculas, sin espacios.

```yaml
---
title: CS149 Parallel Computing
descripcion: Un párrafo corto que aparece en la portada y en la página del curso.
institucion: Stanford
periodo: Fall 2023
orden: 1
sitio: https://gfxcourses.stanford.edu/cs149/fall23
---
```

- `orden` define la posición en la portada. Un curso sin `orden` va al final.
- `institucion`, `periodo` y `sitio` son opcionales; si faltan, no se muestran.
- El cuerpo del archivo (debajo del front matter) es opcional y aparece después de la
  descripción.

## Agregar una clase

Crear `_clases/<curso>/claseNN.md`, con el número en dos dígitos: `clase01.md`,
`clase02.md`, …, `clase12.md`.

```yaml
---
curso: cs149
numero: 1
title: Título de la clase
resumen: Una línea que aparece en la lista de clases del curso.
slides: https://link-a-las-slides
video: https://link-al-video
fecha: 2023-09-12
---
```

- `slides`, `video` y `fecha` son opcionales. Los links que falten no se muestran.
- `fecha` es cuándo escribí el resumen y se muestra como "12 de septiembre de 2023".
- El orden en el curso y la navegación anterior/siguiente salen de `numero`.

### Links internos y rutas de imágenes

Vale igual para clases y assignments.

- **Los links a otras páginas del sitio van siempre con el tag `link` apuntando al
  archivo**, nunca con rutas escritas a mano:

  ```markdown
  Esto sigue en la [clase 2]({% link _clases/cs149/clase02.md %}).
  ```

  El tag agrega el baseurl solo (en Pages el sitio vive bajo `/suipaya/`) y rompe el
  build con `Could not find document` si el archivo no existe, así que un link roto se
  detecta antes de publicar.

- **En los tags de figuras la ruta de la imagen va sin barra inicial**:
  `assets/img/figura.svg`, no `/assets/img/figura.svg`. El plugin antepone el baseurl y
  una barra; con barra inicial, en local queda `//assets/img/figura.svg`, que el
  navegador interpreta como otro dominio y la imagen no carga.

## Agregar un assignment

Crear `_assignments/<curso>/assignmentN.md`, con el número sin ceros: `assignment1.md`,
`assignment2.md`.

```yaml
---
curso: cs149
numero: 1
title: Título del assignment
resumen: Una línea que aparece en la lista de assignments del curso.
enunciado: https://link-al-enunciado-oficial
repo: https://github.com/gpylypchuk/mi-solucion
fecha: 2023-10-01
---
```

`enunciado`, `repo` y `fecha` son opcionales. Si un curso no tiene assignments, la
sección no aparece en su página.

## Cuidado con el campo `curso`

El campo `curso` de cada clase y assignment tiene que coincidir exactamente con el nombre
del archivo del curso, sin extensión y en minúsculas: `curso: cs149` para
`_cursos/cs149.md`. La comparación es de texto exacto. Si no coincide (`CS149`, `cs-149`,
un espacio de más), la clase no aparece en el curso, no tiene link de vuelta ni
navegación, y el build no da ningún error.

## Nombres de archivo y URLs

Clases y assignments comparten el esquema de URL `/<curso>/<nombre-del-archivo>/`. Por
eso hay que respetar la convención `claseNN.md` y `assignmentN.md`: dos archivos con el
mismo nombre dentro de un curso, uno en `_clases` y otro en `_assignments`, generarían la
misma URL y uno pisaría al otro.

## Tags del tema

Todos los argumentos van entre comillas. El texto admite markdown en línea.

**Sidenote** (nota numerada al margen):

```liquid
{% sidenote 'sn-id' 'Texto de la nota.' %}
```

**Marginnote** (nota al margen sin número):

```liquid
{% marginnote 'mn-id' 'Texto de la nota.' %}
```

**Figura al margen** (la ruta es relativa a la raíz del sitio, sin barra inicial):

```liquid
{% marginfigure 'mf-id' 'assets/img/figura.png' 'Epígrafe de la figura.' %}
```

**Figura en la columna principal**:

```liquid
{% maincolumn 'assets/img/figura.png' 'Epígrafe de la figura.' %}
```

**Figura a todo el ancho**:

```liquid
{% fullwidth 'assets/img/figura.png' 'Epígrafe de la figura.' %}
```

**Newthought** (comienzo de sección en versalitas):

```liquid
{% newthought 'Las primeras palabras' %} y el resto del párrafo.
```

**Epígrafe**:

```liquid
{% epigraph 'Texto de la cita.' 'Autor' 'Obra' %}
```

### Dos avisos sobre las notas

- **Cada sidenote, marginnote y figura al margen necesita un id único dentro de la
  página.** El id se usa para el botón que despliega la nota en celular; si dos notas
  comparten id, tocar una abre la otra. Entre páginas distintas el id se puede repetir.
- **Un apóstrofe dentro de una nota entre comillas simples la rompe.** Los argumentos se
  separan como en una terminal, así que el apóstrofe cierra la comilla. Con un solo
  apóstrofe (`'la nota de Juan's'`) el build falla con `Unmatched quote`; con dos
  (`'rock'n'roll'`) no hay error, pero los apóstrofes desaparecen y queda `rocknroll`.
  Si el texto lleva un apóstrofe, escribirlo entre comillas dobles:

  ```liquid
  {% sidenote 'sn-id' "Una nota con rock'n'roll." %}
  ```

## Ecuaciones

Las ecuaciones se escriben con `$$`, la sintaxis nativa de kramdown, y las renderiza
MathJax 3.

Fórmula en línea: `$$` dentro de un párrafo.

```markdown
El speedup es $$S = T_1 / T_p$$ para p procesadores.
```

Ecuación centrada: un bloque `$$` en su propio párrafo, con una línea vacía antes y
después.

```markdown
Texto anterior.

$$
S(p) = \frac{1}{(1 - f) + \frac{f}{p}}
$$

Texto posterior.
```

## Código y tablas

Los bloques de código van con triple backtick y el lenguaje (```` ```c ````,
```` ```python ````), con resaltado de Rouge. Las tablas usan la sintaxis de markdown,
con `:` para alinear columnas:

```markdown
| Versión   | Tiempo (ms) |
|:----------|------------:|
| Ejemplo A |         100 |
```

En `_clases/cs149/clase01.md` hay un ejemplo de cada elemento.
