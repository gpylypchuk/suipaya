---
curso: cs149
nota: true
title: Cómo ejecuta instrucciones un núcleo moderno
---

## El núcleo

{% newthought 'Un núcleo moderno es paralelo' %} en cuatro niveles, y el slide de la
clase, con un núcleo Intel Skylake, los muestra todos.

{% maincolumn 'assets/img/cs149/clase02/slide-skylake-core.jpg' 'Fuente: Stanford CS149, Fall 2023, clase 2.' %}

- **Superescalar.** Seis Fetch/Decode lanzan varias instrucciones del mismo thread por
  ciclo, sin intervención del programador.
- **SMT.** Dos *execution contexts*{% sidenote 'sn-contexto' 'El estado de un thread dentro del núcleo: sus registros y su *program counter*.' %}
  permiten que dos threads compartan las mismas unidades.
- **SIMD.** Cada unidad vectorial aplica una instrucción a 8 `float` a la vez; la
  aprovechan el compilador o el programador, con intrinsics o ISPC.
- **Multi-core.** El chip repite el núcleo entero, y repartir el trabajo entre núcleos es
  tarea del programador.

{% maincolumn 'assets/img/cs149/clase02/nucleo.svg' 'El mismo núcleo, esquematizado. Por ciclo lanza hasta 4 instrucciones escalares y 3 vectoriales, con 2 multiplicaciones vectoriales como máximo.' %}

## Superescalar e ILP

{% newthought 'Un procesador escalar' %} lanza una instrucción por ciclo, en orden. Uno
superescalar lanza en el mismo ciclo todas las que no dependen entre sí. Con este programa,

```cpp
a = x * 2;   // (1)
b = y + 3;   // (2)
c = z * 5;   // (3)
d = a + b;   // (4) usa (1) y (2)
e = c * d;   // (5) usa (3) y (4)
```

el escalar tarda 5 ciclos y el superescalar 3: lanza (1), (2) y (3) juntas, después (4) y
después (5).

{% fullwidth 'assets/img/cs149/clase02/escalar-superescalar.svg' 'Uno y tres slots de emisión. En rojo, la ruta crítica; en gris, los slots vacíos.' %}

La cantidad de instrucciones independientes que ofrece un programa es su **ILP**
(*instruction-level parallelism*). El hardware la extrae solo, a partir de código
secuencial. Se mide con el **IPC**, las instrucciones completadas por ciclo:

$$
\text{IPC} = \frac{\text{instrucciones}}{\text{ciclos}}.
$$

El escalar da $$\text{IPC} = 1$$ y el superescalar $$5/3 \approx 1{,}67$$. El techo lo pone
la **ruta crítica**, la cadena de dependencias más larga: (1)&nbsp;→&nbsp;(4)&nbsp;→&nbsp;(5) necesita 3 ciclos
aunque el núcleo tenga infinitas unidades.{% sidenote 'sn-ruta' '(2) → (4) → (5) es igual de larga. La ruta crítica no tiene por qué ser única.' %}

## Dependencias y latencia

{% newthought 'Una instrucción no entrega' %} su resultado en el ciclo en que sale. La
**latencia** es cuántos ciclos tarda, y la instrucción que necesita ese resultado espera.{% sidenote 'sn-skylake' 'En Skylake, una multiplicación de punto flotante tiene unos 4 ciclos de latencia.' %}
Es lo que pasa en el `while` de `clampedExp`, en el Prog 2 de la asst1:

```cpp
while (count > 0) {
    result = result * x;   // usa el anterior
    count--;
}
```

Cada multiplicación espera a la anterior y sale una cada 4 ciclos. Las dos unidades
podrían empezar una multiplicación por ciclo cada una, así que 7 de cada 8 slots quedan
vacíos (fila a).

{% fullwidth 'assets/img/cs149/clase02/latencia-smt-acumuladores.svg' 'Dos unidades de multiplicación durante 12 ciclos: 24 slots. En gris, los vacíos.' %}

## Out-of-order

{% newthought 'El núcleo mantiene una ventana' %} de instrucciones pendientes{% sidenote 'sn-ventana' 'Unas 200 instrucciones; en Skylake son 224.' %}
y en cada ciclo lanza las que ya tienen sus datos, aunque estén más adelante en el
programa. Eso es la
ejecución **out-of-order**. Los resultados se confirman en el orden original.

Dos mecanismos la sostienen. El **renombrado de registros** asigna registros físicos
distintos a instrucciones que reutilizan un registro sin compartir datos, y así elimina
dependencias falsas. Las unidades **segmentadas** (*pipelined*) aceptan una operación nueva
por ciclo mientras las anteriores avanzan: la latencia dice cuánto tarda un resultado, y el
**throughput**, cuántas operaciones nuevas empiezan por ciclo. Contra una dependencia real,
como la de `clampedExp`, la ventana no ayuda: no hay nada que adelantar.

## Hyperthreading (SMT)

{% newthought 'Si un thread no tiene' %} suficiente ILP, otro puede aportar el suyo. Eso
es el **multithreading simultáneo** (SMT), que Intel llama *hyperthreading*: el núcleo
guarda el estado de dos threads y en cada ciclo lanza instrucciones de cualquiera de los
dos. Como un thread nunca depende del otro, esas instrucciones siempre son independientes
(fila b).

Lo único que se duplica es el estado: registros y *program counter*. Las ALUs, los
Fetch/Decode y las cachés se comparten, así que el SMT no da 2x; la mejora típica va de 0 %
a 30 %, y es mayor cuanto más esperan los threads por latencia o por memoria. Se ve en el
Prog 1: en las máquinas myth, de 4 núcleos con hyperthreading, el speedup sigue subiendo un
poco de 4 a 8 threads. En un i5-8400{% sidenote 'sn-coffee' 'Coffee Lake: el núcleo de Skylake, 6 por chip y sin hyperthreading.' %}
pasar de 6 a 7 threads lo empeora, porque el thread extra no tiene contexto propio y
comparte un núcleo por turnos.

## ILP por software

{% newthought 'Un solo thread también' %} puede ofrecer cadenas independientes. Con un
acumulador, cada multiplicación espera a la anterior; con varios, las cadenas se intercalan:

```cpp
float r0 = 1, r1 = 1, r2 = 1, r3 = 1;
for (int i = 0; i < N; i += 4) {
    // 4 cadenas independientes
    r0 *= a[i];   r1 *= a[i+1];
    r2 *= a[i+2]; r3 *= a[i+3];
}
float r = (r0 * r1) * (r2 * r3);
```

Para llenarlas, tiene que haber una operación en vuelo por unidad y por ciclo de
latencia:

$$
\text{cadenas necesarias} = \text{latencia} \times \text{unidades} = 4 \times 2 = 8.
$$

Con cuatro cadenas se usa la mitad de los slots (fila c). Con menos de ocho quedan huecos, y
con más no se gana nada.{% sidenote 'sn-simulador' 'Lo mismo pasa con el único acumulador de `arraySumVector`, en el Prog 2, pero el simulador de CS149 no lo refleja: cuenta instrucciones, no latencias.' %}

## Pico teórico del i5-8400

{% newthought 'Multiplicando los niveles' %} se obtiene el máximo del procesador. Para un
i5-8400, con 6 núcleos a unos 3,8 GHz{% sidenote 'sn-turbo' 'Con los 6 núcleos activos; la frecuencia base es 2,8 GHz.' %}
y contando solo multiplicaciones de `float`:

$$
\underbrace{2}_{\text{unidades de mul}} \times
\underbrace{8}_{\text{lanes}} \times
\underbrace{6}_{\text{núcleos}} \times
\underbrace{3{,}8 \times 10^9}_{\text{ciclos/s}}
\approx 365 \times 10^9 \ \text{mult/s}.
$$

Un programa escalar de un thread, con una multiplicación por ciclo, hace unas $$3{,}8 \times 10^9$$
por segundo: casi 100 veces menos. La asst1 recorre esa distancia factor por factor. Los 6
núcleos se aprovechan con threads en el Prog 1 y con tasks de ISPC en el Prog 3. Las 8
lanes, con SIMD simulado en el Prog 2 y con ISPC sobre AVX2 en los Prog 3 a 5. El último ×2
exige ocultar la latencia con cadenas independientes: el out-of-order las aprovecha, pero
solo si el código las ofrece.
