---
curso: cs149
numero: 1
title: Clase de ejemplo 1
resumen: Resumen de ejemplo en una línea, se reemplaza por el definitivo.
slides:
video:
fecha: 2023-09-12
---

{% newthought 'Este es un texto de ejemplo' %} que muestra cada elemento del tema. El
contenido real de la clase se escribe después, reemplazando estos párrafos.

## Notas al margen

Un párrafo con una sidenote numerada{% sidenote 'sn-ejemplo-1' 'Texto de ejemplo de una sidenote. En pantallas angostas se despliega al tocar el número.' %}
y otro con una marginnote sin número.{% marginnote 'mn-ejemplo-1' 'Texto de ejemplo de una marginnote.' %}
Si una nota lleva un apóstrofe se escribe entre comillas dobles.{% sidenote 'sn-ejemplo-2' "Nota de ejemplo con un apóstrofe: rock'n'roll." %}

## Figura al margen

{% marginfigure 'mf-ejemplo-1' 'assets/img/placeholder.svg' 'Figura de ejemplo al margen.' %}
Este párrafo acompaña a una figura al margen. En escritorio la figura aparece a la
derecha; en celular se despliega al tocar el símbolo ⊕.

## Ecuaciones

Una fórmula en línea como $$S = T_1 / T_p$$ queda dentro del párrafo. Una ecuación
centrada va en su propio párrafo:

$$
S(p) = \frac{1}{(1 - f) + \frac{f}{p}}
$$

## Código

```c
for (int i = 0; i < n; i++) {
    y[i] = a * x[i] + y[i];
}
```

## Resultados

| Configuración | Tiempo (ms) | Speedup |
|:--------------|------------:|--------:|
| Ejemplo A     |         100 |    1.0x |
| Ejemplo B     |          50 |    2.0x |
| Ejemplo C     |          25 |    4.0x |

Los valores de la tabla son de ejemplo, no son mediciones reales.
