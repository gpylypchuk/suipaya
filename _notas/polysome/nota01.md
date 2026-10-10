---
proyecto: polysome
numero: 1
title: Fundamentos, de la neurona a la atención
resumen: Qué hace una neurona, por qué existen las activaciones, de dónde sale GELU y qué es la atención.
fecha: 2026-10-10
---

## Qué hace una neurona

{% newthought 'Una neurona hace dos cosas' %} y siempre en el mismo orden. Primero calcula
una suma pesada de sus entradas y le agrega un número fijo, el bias. Después le aplica a
ese resultado una función, la activación. Con tres entradas, la primera parte es

$$
z = w_1 x_1 + w_2 x_2 + w_3 x_3 + b.
$$

Para verlo con números, supongamos que las entradas son 2, −1 y 3, que los pesos son 0,5,
1 y −0,2, y que el bias es 0,1. La suma pesada da

$$
z = 2(0{,}5) + (-1)(1) + 3(-0{,}2) + 0{,}1 = -0{,}5.
$$

Después viene la activación. Con ReLU el resultado es $$\text{ReLU}(-0{,}5) = 0$$, y con
GELU es $$\text{GELU}(-0{,}5) \approx -0{,}154$$. Las dos funciones aparecen con detalle
más abajo.

Conviene separar bien las dos partes. Los pesos y el bias son aprendidos, es decir que
salen del entrenamiento y cada neurona tiene los suyos. La versión más chica de GPT 2
tiene 124.439.808 de estos números, y son justamente lo que guarda el archivo de
pesos.{% sidenote 'sn-parametros' 'ProtGPT2 usa la misma arquitectura en un tamaño más grande y llega a 738 millones de parámetros. El archivo de pesos no guarda nada sobre la activación, porque no hay nada que guardar.' %}
La activación, en cambio, es una fórmula fija. No tiene parámetros, no se entrena y es la
misma para todas las neuronas.{% marginnote 'mn-perillas' 'Los pesos son como perillas de volumen, una por entrada, que deciden cuánto suena cada una en la mezcla. ReLU es un interruptor que deja pasar la señal o la corta. GELU es un dimmer que la atenúa de a poco.' %}

## Por qué hace falta algo no lineal

{% newthought 'Podría parecer' %} que la activación es un detalle, pero sin ella apilar
capas no sirve de nada. Una capa sin activación es una transformación lineal más un bias,
$$W_1 x + b_1$$. Si encima pongo otra capa igual, queda

$$
\begin{aligned}
W_2(W_1 x + b_1) + b_2 &= (W_2 W_1)\,x + (W_2 b_1 + b_2) \\
&= W x + b,
\end{aligned}
$$

con $$W = W_2 W_1$$ y $$b = W_2 b_1 + b_2$$. Las dos capas colapsan en una sola, y lo mismo
pasa con diez o con cien.{% marginnote 'mn-zoom' 'Es como hacer zoom dos veces sobre una foto. El resultado es el mismo que un solo zoom más grande, y apilar zooms no agrega nada nuevo.' %}

Una transformación lineal solo puede rotar, estirar y proyectar el espacio. No puede
expresar condiciones del tipo "si este patrón aparece, hacé tal cosa", porque su respuesta
es siempre proporcional a la entrada y no tiene umbrales. La activación agrega justamente
eso, un comportamiento que cambia según el valor que le llega.

## Capas y MLP

{% newthought 'Una capa son muchas neuronas' %} trabajando en paralelo sobre las mismas
entradas. Cada neurona tiene su propia fila de pesos, y si apilo esas filas obtengo una
matriz $$W$$. Calcular todas las neuronas juntas es entonces una multiplicación de matriz
por vector,

$$
y = W x + b,
$$

donde cada componente de $$y$$ es la suma pesada de una neurona. Por eso la
multiplicación de matrices es la operación central de todo el motor.

El MLP de GPT 2 son dos capas de este tipo con una GELU en el medio. La primera lleva cada
token de 768 números a 3072, después se aplica GELU a cada uno de esos 3072 números, y la
segunda vuelve a 768.

$$
\text{MLP}(x) = W_2\,\text{GELU}(W_1 x + b_1) + b_2
$$

En ProtGPT2 los tamaños son 1280 y 5120. Hay un detalle que importa mucho más adelante. El
MLP procesa cada token solo, sin mirar a los demás.

## ReLU

{% newthought 'La activación más simple' %} que funciona bien es ReLU, que deja pasar los
positivos y convierte los negativos en cero.

$$
\text{ReLU}(x) = \max(0, x) = x \cdot \mathbf{1}[x > 0]
$$

La segunda forma se lee como una compuerta. El factor $$\mathbf{1}[x > 0]$$ vale 1 si
$$x$$ es positivo y 0 si no, así que ReLU multiplica la entrada por una compuerta que está
abierta o cerrada.

Tiene dos problemas. El primero es el quiebre en cero, donde la pendiente cambia de golpe
y la derivada no está definida. El segundo es más serio. Para cualquier valor negativo el
gradiente es cero, así que si una neurona queda recibiendo solo sumas negativas, deja de
aprender y no tiene forma de salir de ahí. A eso se le dice una neurona
muerta.{% sidenote 'sn-relu-muerta' 'En inglés se habla de *dying ReLU*. Pasa más con learning rates altos, cuando una actualización grande empuja los pesos o el bias a una zona donde la suma es siempre negativa.' %}

## GELU

{% newthought 'GELU reemplaza' %} la compuerta de golpe de ReLU por una suave. En vez de
multiplicar $$x$$ por 0 o por 1, lo multiplica por un número entre 0 y 1 que crece con
$$x$$.

$$
\text{GELU}(x) = x\,\Phi(x), \qquad \Phi(x) = \tfrac{1}{2}\left(1 + \operatorname{erf}\left(\tfrac{x}{\sqrt{2}}\right)\right)
$$

Acá $$\Phi$$ es la distribución acumulada de la normal estándar, o sea la probabilidad de
que una variable normal con media 0 y desvío 1 sea menor que
$$x$$.{% sidenote 'sn-gelu-paper' 'Hendrycks y Gimpel (2016), *Gaussian Error Linear Units (GELUs)*, arXiv 1606.08415.' %}

La intuición viene de pensarla como una máscara aleatoria. Imaginemos que multiplico $$x$$
por una variable $$m$$ que vale 1 con probabilidad $$\Phi(x)$$ y 0 en el resto de los
casos, así que cuanto más grande es $$x$$, más probable es que pase. El valor esperado de
esa salida es

$$
\mathbb{E}[x\,m] = x \cdot 1 \cdot \Phi(x) + x \cdot 0 \cdot \bigl(1 - \Phi(x)\bigr) = x\,\Phi(x),
$$

que es exactamente GELU. La red no sortea nada y usa directamente el promedio.

Hay tres regímenes. Para $$x$$ grande, $$\Phi(x)$$ es casi 1 y GELU da aproximadamente
$$x$$, igual que ReLU. Para $$x$$ muy negativo, $$\Phi(x)$$ es casi 0 y GELU da
aproximadamente 0. Cerca de cero hay una transición suave, y como ahí $$x$$ es negativo
pero $$\Phi(x)$$ todavía no es cero, la salida queda un poco por debajo de cero. Eso forma
un valle cuyo mínimo es $$\approx -0{,}17$$ en $$x \approx -0{,}75$$. Redondeando a tres
decimales, $$\text{GELU}(1) = 0{,}841$$, $$\text{GELU}(-1) = -0{,}159$$ y
$$\text{GELU}(2) = 1{,}954$$.

{% maincolumn 'assets/img/proyectos/polysome/relu_gelu.svg' 'ReLU y GELU exacta entre −4 y 4. Lejos del cero las dos curvas casi coinciden, y cerca del cero GELU dibuja un valle suave en lugar de un quiebre.' %}

## La aproximación con tanh

{% newthought 'El mismo paper' %} propone una aproximación con tanh para cuando la
velocidad importa más que la exactitud. La idea es que tanh y erf tienen la misma forma de
S, así que alcanza con ajustar el argumento. La forma general es

$$
\Phi(x) \approx \tfrac{1}{2}\Bigl(1 + \tanh\bigl(k\,(x + a\,x^3)\bigr)\Bigr),
$$

y hay que elegir las constantes $$k$$ y $$a$$.

La constante $$k$$ sale de igualar la pendiente en cero. La derivada de $$\Phi$$ es la
densidad normal, así que $$\Phi'(0) = 1/\sqrt{2\pi}$$. Del lado derecho, como
$$\tanh'(0) = 1$$, la derivada en cero es $$\tfrac{1}{2}k$$. Igualando las dos,

$$
\tfrac{1}{2}k = \frac{1}{\sqrt{2\pi}} \quad\Longrightarrow\quad k = \sqrt{\frac{2}{\pi}} \approx 0{,}7979.
$$

La constante $$a$$ sale de comparar los desarrollos de Taylor hasta $$x^3$$. Del lado
izquierdo,

$$
\Phi(x) = \tfrac{1}{2} + \frac{1}{\sqrt{2\pi}}\left(x - \frac{x^3}{6} + \dots\right).
$$

Del lado derecho uso $$\tanh(u) = u - u^3/3 + \dots$$ con $$u = kx + ka\,x^3$$, y me quedo
solo con los términos hasta $$x^3$$,

$$
\tfrac{1}{2}\bigl(1 + \tanh(u)\bigr) = \tfrac{1}{2} + \tfrac{1}{2}k\,x + \tfrac{1}{2}\left(ka - \frac{k^3}{3}\right)x^3 + \dots
$$

Los coeficientes de $$x$$ ya coinciden por la elección de $$k$$. Igualando los de $$x^3$$,
y usando que $$1/\sqrt{2\pi} = k/2$$, queda

$$
\tfrac{1}{2}\left(ka - \frac{k^3}{3}\right) = -\frac{k}{12}
\quad\Longrightarrow\quad
a = \frac{k^2}{3} - \frac{1}{6} = \frac{2}{3\pi} - \frac{1}{6} \approx 0{,}0455.
$$

El valor que se usa en la práctica es 0,044715, un poco menor. No sale de Taylor sino de
un ajuste numérico que minimiza el error en todo el rango y no solo cerca de cero, que es
donde Taylor es bueno. La fórmula final queda

$$
\text{GELU}(x) \approx \tfrac{1}{2}\,x\left(1 + \tanh\left(\sqrt{\tfrac{2}{\pi}}\,\bigl(x + 0{,}044715\,x^3\bigr)\right)\right).
$$

Esta es la versión con la que se entrenó GPT 2.{% sidenote 'sn-gelu-new' 'En HuggingFace esta versión se llama `gelu_new`, y la exacta con erf se llama `gelu`.' %}

## Atención

{% newthought 'El MLP solo no alcanza' %}, porque procesa cada token aislado. En la frase
"el perro que vi ayer ladraba", para entender "ladraba" hay que saber quién ladraba, y la
respuesta está varias palabras atrás, en "perro". Ningún cálculo que mire un token por vez
puede encontrar esa relación.

La atención es el mecanismo que deja que los tokens se miren entre sí. Cada token genera
tres vectores a partir de sus números, una pregunta que se llama query, una etiqueta que
se llama key y una información que se llama value. Después compara su pregunta con las
etiquetas de los tokens anteriores. Cuanto mejor coincide con una etiqueta, más peso le da
a ese token, y el resultado es un promedio ponderado de las informaciones de todos
ellos.{% sidenote 'sn-causal' 'Mira solo hacia atrás porque el modelo genera de izquierda a derecha. Cuando predice el token siguiente, los posteriores todavía no existen.' %}
En el ejemplo, la pregunta de "ladraba" busca quién hace la acción, la etiqueta de "perro"
coincide bien, y la salida de "ladraba" se lleva una buena parte de la información de
"perro".{% marginnote 'mn-biblioteca' 'Es parecido a buscar en una biblioteca. La query es lo que ando buscando, la key es el título en el lomo de cada libro y el value es lo que el libro tiene adentro. Me llevo un poco de cada libro según cuánto se parece su título a lo que busco.' %}

En proteínas pasa lo mismo. El aminoácido de la posición 50 puede depender del de la
posición 10, porque cuando la cadena se pliega los dos quedan juntos en el espacio aunque
en la secuencia estén lejos. Las fórmulas del mecanismo quedan para una nota futura, y
acá alcanza con la idea.

## Cómo encaja todo

{% newthought 'Con estas piezas' %} ya se puede ver el recorrido completo de GPT 2 en su
versión más chica.

```text
texto → tokens → cada token se vuelve 768 números
      → [ atención (los tokens se miran entre sí)
          MLP (cada token se procesa solo, con GELU adentro) ] × 12 bloques
      → probabilidad del siguiente token
```

Cada bloque alterna las dos cosas. Primero la atención mezcla información entre tokens, y
después el MLP procesa cada token por separado. ProtGPT2 tiene la misma estructura con
1280 números por token y 36 bloques.

## Qué implica para el motor

{% newthought 'Para el motor' %} todo esto deja tres consecuencias concretas.

La primera es que hay que usar la versión con tanh. Los pesos se entrenaron con ella, y el
test que compara contra PyTorch la espera. Si uso erf, el test falla por precisión. El
error es chico y aparece en todos los elementos a la
vez,{% sidenote 'sn-error-erf' 'La diferencia máxima entre las dos versiones es de unos 0,00047 y aparece cerca de x = 2,7 y x = −2,7.' %}
que es una firma muy distinta de la de un bug de índices, donde algunos elementos dan
cualquier cosa y otros dan perfecto.

La segunda es que GELU es una operación elemento por elemento. Cada número se transforma
solo, sin mirar a sus vecinos, así que se puede hacer in place sobre el mismo buffer. Todo
va en float, con la constante escrita como `0.044715f`, `tanhf` en lugar de `tanh` y el
cubo como `x*x*x`.{% sidenote 'sn-float' 'Sin la f, la constante es un double y arrastra toda la cuenta a double. En una GPU de consumo como la 2060 Super el double rinde una fracción mínima de lo que rinde el float.' %}

```cpp
void gelu_inplace(float* data, int n) {
    const float k = 0.7978845608f;  // sqrt(2/pi)
    for (int i = 0; i < n; i++) {
        float x = data[i];
        data[i] = 0.5f * x * (1.0f + tanhf(k * (x + 0.044715f * x*x*x)));
    }
}
```

La tercera es el costo. La cuenta es barata, unas pocas multiplicaciones y una tanh por
elemento. En la GPU lo que cuesta es leer cada número de memoria y volver a escribirlo, no
calcular. Por eso en el hito M04 se fusiona con la suma del bias que viene justo antes, y
así cada número se lee y se escribe una sola vez en lugar de
dos.{% marginnote 'mn-almacen' 'Es como ir dos veces al almacén por dos cosas que se podían comprar en un solo viaje. Lo caro es el viaje y no lo que se compra.' %}
