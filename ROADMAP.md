# ROADMAP. Sitio de cursos con tema Tufte

## Contexto
Quiero un sitio personal estático, en español, con el estilo visual de siboehm.com
(tema Tufte para Jekyll). La portada lista cursos como si fueran blogposts. Cada curso
tiene una página con sus clases y sus assignments, y cada clase o assignment tiene su
propia página con un resumen escrito por mí y sidenotes al margen.

## Decisiones ya tomadas
1. Repo propio (este, gpylypchuk.github.io), no fork. El tema base se copia de
   github.com/clayh53/tufte-jekyll y se conserva su LICENSE MIT intacto.
2. Jekyll 4.3 usando los plugins Ruby del tema (carpeta _plugins).
3. Deploy con GitHub Actions, porque el build clásico de Pages no ejecuta plugins propios.
4. Todo el texto visible en castellano.

## Reglas de trabajo
Trabajá una fase por vez. Al terminar cada fase corré bundle exec jekyll build, hacé un
commit con el mensaje "Fase N, descripción corta", resumí qué cambiaste y frená hasta que
te diga que sigas. No inventes contenido real de los cursos, usá placeholders. No agregues
frameworks de JavaScript ni dependencias nuevas sin preguntarme. Los estilos nuevos van en
el SCSS del tema, usando sus variables de color y tipografía.

## Referencia visual
Fondo crema, texto casi negro, rojo oscuro como color de contraste para links y títulos de
la portada, serif ETBembo del tema para el cuerpo. Header arriba a la izquierda en sans
serif, versalitas con letter spacing amplio, en rojo, con el logo <SUIPAYA> y al lado el
link SOBRE MÍ. Portada con el título del sitio grande y en minúscula, una línea de
presentación y debajo la lista de cursos con viñetas, cada uno con su título grande en rojo
y un párrafo justificado de descripción. Si existe referencia/siboehm.png, usala como guía.

## Estructura final esperada
_config.yml
Gemfile
index.html
sobre.md
_cursos/
    cs149.md
    ddca.md
_clases/
    cs149/
        clase01.md
        clase02.md
_assignments/
    cs149/
        assignment1.md
_layouts/
    curso.html
    clase.html
    assignment.html
_data/
    meses.yml
    social.yml
.github/workflows/pages.yml

## Fase 1. Base del tema
Copiá el contenido de github.com/clayh53/tufte-jekyll a este repo sin su carpeta .git.
Conservá LICENSE. Borrá los posts de ejemplo, _drafts, los Rakefiles, _page.txt, _post.txt,
la página about de ejemplo, feed.xml y la imagen badge. Creá un Gemfile con jekyll 4.3 y
rouge, y un .gitignore con _site, .jekyll-cache y .bundle.
Terminado cuando el build compila sin errores y no queda contenido de ejemplo del tema.

## Fase 2. Configuración y español
En _config.yml poné title suipaya, author Geronimo Pylypchuk, una description corta,
baseurl vacío, url apuntando a gpylypchuk.github.io con https, lang es y timezone
America/Argentina/Buenos_Aires. Sacá el permalink de articles y las claves de los Rakefiles
(post, page, editor, git, transfer). Agregá lang="es" al elemento html y hyphens auto al
texto justificado para que corte bien las palabras en castellano. Traducí todos los textos
de la interfaz. Creá _data/meses.yml con los meses en castellano para mostrar fechas como
"12 de septiembre de 2023". En _data/social.yml dejá solo GitHub (gpylypchuk). En el footer
sacá el mailto de ejemplo y el ícono de RSS, y agregá la línea "Tema basado en tufte jekyll
de Clay Harmon".
Terminado cuando no queda ningún texto en inglés en la interfaz.

## Fase 3. Header y portada
Header fijo con el logo de texto <SUIPAYA> linkeado al inicio y el link SOBRE MÍ, con el
estilo de la referencia visual. No iterar site.pages para el menú, dejarlo explícito.
Portada con el título grande suipaya, la línea "Este es el sitio de Geronimo Pylypchuk." y
la lista de cursos como blogposts. Cada ítem muestra solo el título del curso en rojo,
linkeado a su página, y su descripción debajo. Nada más, ni fechas ni clases. El orden lo
define el campo orden de cada curso. Página sobre.md simple con placeholder, en /sobre/.
Terminado cuando la portada se parece a la referencia en escritorio y en celular.

## Fase 4. Cursos, clases y assignments
Tres colecciones con output activado.
_cursos, un archivo por curso con los campos title (se llama así para que el tema lo use
en el head), descripcion, institucion, periodo, orden, slug y sitio (link a la página
oficial). Cada curso queda en /slug/, por ejemplo /cs149/.
_clases, una subcarpeta por curso y un archivo por clase con los campos curso, numero,
title, resumen de una línea, slides y video (links a los originales) y fecha opcional
(cuándo lo escribí). El permalink sale de la ruta del archivo, así
_clases/cs149/clase01.md queda en /cs149/clase01/.
_assignments, misma estructura con los campos curso, numero, title, resumen, enunciado
(link oficial), repo (link a mi código, opcional) y fecha opcional.
_assignments/cs149/assignment1.md queda en /cs149/assignment1/.
Layout curso. Título, institución y período en una línea, descripción y link al sitio
oficial. Después una sección Clases con la lista ordenada por numero, cada ítem con
"Clase N", título linkeado y resumen de una línea. Después una sección Assignments con el
mismo formato. Si un curso no tiene assignments, esa sección no se muestra.
Layout clase, basado en el layout post del tema. Arriba un link de vuelta al curso, la
etiqueta "Clase N" sobre el título y una línea con los links a slides y video (solo los
que existan). Si hay fecha, mostrala en castellano. Abajo navegación anterior y siguiente
dentro del mismo curso, ordenada por numero.
Layout assignment, igual que clase pero con la etiqueta "Assignment N" y links a enunciado
y repo en lugar de slides y video.
Terminado cuando se puede navegar portada, curso, clase, siguiente clase y volver.

## Fase 5. Contenido inicial
Creá dos cursos. CS149 Parallel Computing (Stanford, Fall 2023, orden 1) y Digital Design
and Computer Architecture (ETH Zürich, Onur Mutlu, período a definir, orden 2), con
descripciones placeholder. Para CS149 creá dos clases y un assignment de ejemplo con texto
placeholder que usen sidenote, marginnote, una figura al margen, una ecuación, un bloque de
código y una tabla de resultados. Documentá en el README cómo agregar un curso, una clase y
un assignment, con un ejemplo de front matter de cada uno, la sintaxis de cada tag del tema
y el aviso de que cada sidenote necesita un id único por página y de que un apóstrofe
dentro de una nota entre comillas simples la rompe.
Terminado cuando las páginas de ejemplo muestran cada elemento correctamente.

## Fase 6. Deploy
Creá .github/workflows/pages.yml basado en el starter oficial de Jekyll para GitHub Pages
(setup de Ruby con cache de bundler, build con bundle exec jekyll build usando el baseurl
que devuelve configure pages, upload del artefacto y deploy). Que corra en cada push a main.
Terminado cuando el workflow queda commiteado; yo activo Pages y hago el push.

## Fase 7. Verificación
Levantá el sitio con bundle exec jekyll serve y revisá
1. Que no haya links rotos entre portada, cursos, clases y assignments.
2. Que las sidenotes aparezcan en el margen en escritorio y se desplieguen al tocar el
   número con menos de 760 px de ancho.
3. Que fechas y textos estén en castellano y el texto justificado corte palabras bien.
4. Que el header, la portada y las páginas internas se vean bien en celular.
Reportame cualquier problema que encuentres antes de darlo por cerrado.