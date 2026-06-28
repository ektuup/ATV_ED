import sys, os, time, re, csv, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6 import QtWidgets, QtCore

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from natives     import Dict, List, Set, Tuple
from specialized import NamedTuple, Deque, ChainMap, Counter, OrderedDict, DefaultDict

SEARCH_WORDS = [
    "Lisbon", "NASA", "Kyunghee", "Konkuk", "Sogang",
    "momentarily", "rubella", "vaccinations", "government", "Authorities",
]

ALL_CLASSES = [
    ("dict",        Dict),
    ("list",        List),
    ("set",         Set),
    ("tuple",       Tuple),
    ("namedtuple",  NamedTuple),
    ("deque",       Deque),
    ("ChainMap",    ChainMap),
    ("Counter",     Counter),
    ("OrderedDict", OrderedDict),
    ("defaultdict", DefaultDict)
]

def tokenize(text):
    return [w for w in re.split(r"[\s\d.,;:!?\"'()\[\]{}<>/\\|@#$%^&*+=`~]+", text) if w]

# ── worker ────────────────────────────────────────────────────────────────────

class BenchWorker(QtCore.QThread):
    progress = QtCore.Signal(str)
    done     = QtCore.Signal(dict)   # always emitted, even on error

    def __init__(self, filepath, mode, words):
        super().__init__()
        self.filepath = filepath
        self.mode     = mode
        self.words    = words

    def run(self):
        try:
            self.progress.emit("Lendo arquivo…")
            with open(self.filepath, "r", encoding="utf-8", errors="replace") as f:
                tokens = tokenize(f.read())

            results = {}
            for label, cls in ALL_CLASSES:
                self.progress.emit(f"{label}…")
                obj = cls()

                if self.mode == "insert":
                    t0 = time.perf_counter()
                    for w in tokens:
                        obj.put(w)
                    results[label] = (time.perf_counter() - t0) * 1000

                else:
                    for w in tokens:
                        obj.put(w)
                    op = obj.get if self.mode == "search" else obj.delt
                    timings = []
                    for w in self.words:
                        t0 = time.perf_counter()
                        op(w)
                        timings.append(time.perf_counter() - t0)
                    results[label] = (sum(timings) / len(timings)) * 1000

            self.done.emit(results)

        except Exception as e:
            self.progress.emit(f"Erro: {e}")
            self.done.emit({})

# ── chart ─────────────────────────────────────────────────────────────────────

class Chart(QtWidgets.QWidget):
    BG     = "#1e1e1e"
    FG     = "#e0e0e0"
    COLORS = ["#9b59b6","#3498db","#2ecc71","#e74c3c",
              "#f39c12","#1abc9c","#e67e22","#e91e8c","#00bcd4","#cddc39"]

    def __init__(self):
        super().__init__()
        self.fig    = Figure(figsize=(6, 3), facecolor=self.BG)
        self.ax     = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.canvas)

    def plot(self, title, results: dict):
        self.ax.clear()
        self.fig.patch.set_facecolor(self.BG)
        self.ax.set_facecolor(self.BG)

        labels = list(results.keys())
        values = list(results.values())
        colors = [self.COLORS[i % len(self.COLORS)] for i in range(len(labels))]

        bars = self.ax.bar(labels, values, color=colors, edgecolor="none", width=0.6)
        mx = max(values) if values else 1
        for bar, v in zip(bars, values):
            self.ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + mx * 0.012,
                f"{v:.3f}", ha="center", va="bottom",
                color=self.FG, fontsize=7.5, fontweight="bold"
            )

        self.ax.set_title(title, color=self.FG, fontsize=10, pad=8)
        self.ax.set_ylabel("ms", color=self.FG, fontsize=9)
        self.ax.tick_params(colors=self.FG, labelsize=8)
        for sp in self.ax.spines.values():
            sp.set_edgecolor("#3a3a3a")
        self.fig.tight_layout()
        self.canvas.draw()

# ── main window ───────────────────────────────────────────────────────────────

# estados possíveis (controle de quais botões ficam ativos)
ST_NO_FILE    = 0   # nenhum arquivo selecionado
ST_READY      = 1   # arquivo selecionado, sem dados inseridos
ST_INSERTED   = 2   # inserção concluída
ST_RUNNING    = 3   # worker em execução

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collections Benchmark")
        self.resize(820, 540)
        self._filepath = None
        self._state    = ST_NO_FILE
        self._build()
        self._style()
        self._apply_state()

    def _build(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        top = QtWidgets.QHBoxLayout()
        self.file_label = QtWidgets.QLabel("Nenhum arquivo selecionado")
        self.file_label.setObjectName("filePath")
        self.btn_file = QtWidgets.QPushButton("Abrir arquivo")
        self.btn_file.clicked.connect(self._pick_file)

        self.btn_ins = QtWidgets.QPushButton("Inserção")
        self.btn_sea = QtWidgets.QPushButton("Busca")
        self.btn_del = QtWidgets.QPushButton("Exclusão")
        self.btn_ins.clicked.connect(lambda: self._run("insert"))
        self.btn_sea.clicked.connect(lambda: self._run("search"))
        self.btn_del.clicked.connect(lambda: self._run("delete"))

        top.addWidget(self.btn_file)
        top.addWidget(self.file_label, 1)
        top.addSpacing(16)
        top.addWidget(self.btn_ins)
        top.addWidget(self.btn_sea)
        top.addWidget(self.btn_del)
        root.addLayout(top)

        self.chart = Chart()
        root.addWidget(self.chart, 1)

        self.status = QtWidgets.QLabel("Selecione um arquivo para começar.")
        self.status.setObjectName("status")
        root.addWidget(self.status)

    def _apply_state(self):
        s = self._state
        self.btn_ins.setEnabled(s in (ST_READY, ST_INSERTED))
        self.btn_sea.setEnabled(s == ST_INSERTED)
        self.btn_del.setEnabled(s == ST_INSERTED)

    def _pick_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Abrir arquivo", "", "Arquivos de texto (*.txt);;Todos (*)"
        )
        if not path:
            return
        self._filepath = path
        self.file_label.setText(os.path.basename(path))
        self._state = ST_READY
        self._apply_state()
        self.status.setText("Arquivo selecionado. Execute a inserção primeiro.")

    def _run(self, mode):
        self._state = ST_RUNNING
        self._apply_state()

        # cria worker sem guardar referência como atributo —
        # o sinal done o mantém vivo até terminar
        worker = BenchWorker(self._filepath, mode, SEARCH_WORDS)
        worker.progress.connect(self.status.setText)
        worker.done.connect(lambda r: self._done(r, mode, worker))
        worker.start()

    def _done(self, results, mode, worker):
        # desconecta tudo antes de qualquer outra coisa
        worker.progress.disconnect()
        worker.done.disconnect()

        if not results:
            self._state = ST_INSERTED if mode != "insert" else ST_READY
            self._apply_state()
            return

        if mode == "insert":
            self._state = ST_INSERTED
        else:
            self._state = ST_INSERTED   # mantém busca/exclusão disponíveis

        self._apply_state()

        titles = {
            "insert": "Inserção — tempo total (ms)",
            "search": "Busca — tempo médio por palavra (ms)",
            "delete": "Exclusão — tempo médio por palavra (ms)",
        }
        self.chart.plot(titles[mode], results)
        self._csv_write(mode, results)
        self.status.setText("Concluído.")

    def _csv_write(self, mode, results):
        path   = "benchmark_results.csv"
        exists = os.path.exists(path)
        ts     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fname  = os.path.basename(self._filepath)
        with open(path, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if not exists:
                w.writerow(["timestamp", "arquivo", "operacao", "estrutura", "tempo_ms"])
            for label, ms in results.items():
                w.writerow([ts, fname, mode, label, f"{ms:.6f}"])

    def _style(self):
        self.setStyleSheet("""
        QWidget { background:#2b2b2b; color:#e0e0e0;
                  font-family:"Segoe UI","Inter",sans-serif; font-size:13px; }
        QPushButton { background:#800080; color:white; border:none;
                      border-radius:4px; padding:6px 14px; font-weight:bold; }
        QPushButton:hover    { background:#9c27b0; }
        QPushButton:pressed  { background:#6a006a; }
        QPushButton:disabled { background:#3a3a3a; color:#555; }
        #filePath { color:#888; font-size:11px; }
        #status   { color:#a5d6a7; font-size:11px; }
        """)

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Window()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
