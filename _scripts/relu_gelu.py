"""Figura de ReLU y GELU exacta para la nota 01 de Polysome.

Genera assets/img/proyectos/polysome/relu_gelu.svg. Se corre desde la raíz del repo,
sin agregar dependencias al sitio:

    uv run --with matplotlib python _scripts/relu_gelu.py
"""

import math
from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "assets/img/proyectos/polysome/relu_gelu.svg"
FUENTE = RAIZ / "fonts/et-book/et-book-roman-line-figures/et-book-roman-line-figures.ttf"

TINTA = "#111111"
GRIS = "#8a8a8a"


def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def gelu(x):
    return x * phi(x)


def relu(x):
    return max(0.0, x)


def main():
    familia = ["serif"]
    if FUENTE.exists():
        font_manager.fontManager.addfont(str(FUENTE))
        familia = [font_manager.FontProperties(fname=str(FUENTE)).get_name(), "serif"]

    plt.rcParams.update({
        "font.family": familia,
        "font.size": 12,
        "axes.unicode_minus": True,
        "svg.fonttype": "path",
        "svg.hashsalt": "suipaya",
    })

    n = 801
    xs = [-4.0 + 8.0 * i / (n - 1) for i in range(n)]

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    ax.plot(xs, [relu(x) for x in xs], color=GRIS, linewidth=1.4, linestyle=(0, (5, 3)), label="ReLU")
    ax.plot(xs, [gelu(x) for x in xs], color=TINTA, linewidth=1.6, label="GELU exacta")

    # Mínimo de GELU, buscado sobre la grilla fina
    x_min = min(xs, key=gelu)
    ax.plot([x_min], [gelu(x_min)], "o", color=TINTA, markersize=4)
    ax.annotate(
        f"mínimo {gelu(x_min):.2f} en x = {x_min:.2f}".replace(".", ",").replace("-", "\u2212"),
        xy=(x_min, gelu(x_min)), xytext=(-3.9, -0.75),
        color=TINTA, fontsize=11, va="center",
        arrowprops={"arrowstyle": "-", "color": GRIS, "linewidth": 0.8},
    )

    ax.legend(loc="upper left", frameon=False, handlelength=2.4, labelcolor=TINTA)

    ax.set_xlim(-4, 4)
    ax.set_ylim(-1, 4)
    ax.set_xticks(range(-4, 5))
    ax.set_yticks(range(-1, 5))
    ax.axhline(0, color=GRIS, linewidth=0.5, zorder=0)
    ax.axvline(0, color=GRIS, linewidth=0.5, zorder=0)

    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(TINTA)
        ax.spines[lado].set_linewidth(0.8)
    ax.tick_params(colors=TINTA, width=0.8, length=4)

    fig.tight_layout()
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, transparent=True, metadata={"Date": None})
    print(f"Figura guardada en {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
