import sys, os, csv
from collections import defaultdict

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6 import QtWidgets

CSV_FILE = "benchmark_results.csv"

BG     = "#1e1e1e"
FG     = "#e0e0e0"
COLORS = ["#9b59b6","#3498db","#2ecc71","#e74c3c",
          "#f39c12","#1abc9c","#e67e22","#e91e8c","#00bcd4","#cddc39",
          "#ff7043","#26c6da","#d4e157"]

def read_csv(path):
    # {operacao: {estrutura: [tempos]}}
    data = defaultdict(lambda: defaultdict(list))
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["operacao"]][row["estrutura"]].append(float(row["tempo_ms"]))
    return data

def make_axes(fig, data, mode, title, pos):
    ax = fig.add_subplot(3, 1, pos)
    ax.set_facecolor(BG)

    structs = list(data[mode].keys())
    means   = [sum(v) / len(v) for v in data[mode].values()]
    colors  = [COLORS[i % len(COLORS)] for i in range(len(structs))]

    bars = ax.bar(structs, means, color=colors, edgecolor="none", width=0.6)
    mx = max(means) if means else 1
    for bar, v in zip(bars, means):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + mx * 0.015,
            f"{v:.3f}", ha="center", va="bottom",
            color=FG, fontsize=7.5, fontweight="bold"
        )

    ax.set_title(title, color=FG, fontsize=10, pad=6)
    ax.set_ylabel("ms", color=FG, fontsize=9)
    ax.tick_params(colors=FG, labelsize=8)
    for sp in ax.spines.values():
        sp.set_edgecolor("#3a3a3a")

def main():
    app = QtWidgets.QApplication(sys.argv)

    path = CSV_FILE
    if not os.path.exists(path):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Abrir CSV", "", "CSV (*.csv)"
        )
        if not path:
            sys.exit(0)

    data = read_csv(path)

    fig = Figure(figsize=(8, 9), facecolor=BG)
    fig.subplots_adjust(hspace=0.55)

    MODES = [
        ("insert", "Inserção — tempo médio (ms)",  1),
        ("search", "Busca — tempo médio (ms)",      2),
        ("delete", "Exclusão — tempo médio (ms)",   3),
    ]
    for mode, title, pos in MODES:
        if mode in data:
            make_axes(fig, data, mode, title, pos)

    win = QtWidgets.QWidget()
    win.setWindowTitle("Resultados")
    win.setStyleSheet("QWidget { background:#2b2b2b; }")
    win.resize(860, 780)

    canvas = FigureCanvas(fig)
    lay = QtWidgets.QVBoxLayout(win)
    lay.setContentsMargins(12, 12, 12, 12)
    lay.addWidget(canvas)

    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
