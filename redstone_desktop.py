from __future__ import annotations

import json
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.logic import comparator_math, farm_plan, gate_truth_table, timing_summary


class RedstonePlannerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sophie Redstone Studio")
        self.resize(900, 620)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.gate_tab = self._build_gate_tab()
        self.compare_tab = self._build_compare_tab()
        self.timing_tab = self._build_timing_tab()
        self.farm_tab = self._build_farm_tab()

        self.tabs.addTab(self.gate_tab, "Gate")
        self.tabs.addTab(self.compare_tab, "Comparator")
        self.tabs.addTab(self.timing_tab, "Timing")
        self.tabs.addTab(self.farm_tab, "Farm")

        self.statusBar().showMessage("Ready")

    def _build_gate_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        controls = QFormLayout()
        self.gate_selector = QComboBox()
        for gate in ["AND", "OR", "XOR", "NAND", "NOR", "NOT"]:
            self.gate_selector.addItem(gate)
        self.gate_inputs = QLineEdit("1, 1")

        controls.addRow("Gate", self.gate_selector)
        controls.addRow("Inputs", self.gate_inputs)
        layout.addLayout(controls)

        self.gate_result = QTextEdit()
        self.gate_result.setReadOnly(True)
        layout.addWidget(self.gate_result)

        actions = QHBoxLayout()
        calc = QPushButton("Calculate")
        calc.clicked.connect(self.calculate_gate)
        save = QPushButton("Export JSON")
        save.clicked.connect(self.export_gate_json)
        actions.addWidget(calc)
        actions.addWidget(save)
        layout.addLayout(actions)

        return page

    def _build_compare_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        controls = QFormLayout()
        self.signal_input = QLineEdit("12")
        self.threshold_input = QLineEdit("9")
        controls.addRow("Signal", self.signal_input)
        controls.addRow("Threshold", self.threshold_input)
        layout.addLayout(controls)

        self.compare_result = QTextEdit()
        self.compare_result.setReadOnly(True)
        layout.addWidget(self.compare_result)

        actions = QHBoxLayout()
        calc = QPushButton("Check")
        calc.clicked.connect(self.calculate_compare)
        save = QPushButton("Export JSON")
        save.clicked.connect(self.export_compare_json)
        actions.addWidget(calc)
        actions.addWidget(save)
        layout.addLayout(actions)

        return page

    def _build_timing_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        controls = QFormLayout()
        self.delay_input = QLineEdit("1")
        self.pulses_input = QLineEdit("4")
        controls.addRow("Repeater delay (ticks)", self.delay_input)
        controls.addRow("Pulses", self.pulses_input)
        layout.addLayout(controls)

        self.timing_result = QTextEdit()
        self.timing_result.setReadOnly(True)
        layout.addWidget(self.timing_result)

        actions = QHBoxLayout()
        calc = QPushButton("Estimate")
        calc.clicked.connect(self.calculate_timing)
        save = QPushButton("Export JSON")
        save.clicked.connect(self.export_timing_json)
        actions.addWidget(calc)
        actions.addWidget(save)
        layout.addLayout(actions)

        return page

    def _build_farm_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        controls = QFormLayout()
        self.farm_selector = QComboBox()
        for farm in ["mob", "iron", "gold", "villager", "crop"]:
            self.farm_selector.addItem(farm)
        controls.addRow("Farm type", self.farm_selector)
        layout.addLayout(controls)

        self.farm_result = QTextEdit()
        self.farm_result.setReadOnly(True)
        layout.addWidget(self.farm_result)

        actions = QHBoxLayout()
        calc = QPushButton("Generate plan")
        calc.clicked.connect(self.calculate_farm)
        save = QPushButton("Export JSON")
        save.clicked.connect(self.export_farm_json)
        actions.addWidget(calc)
        actions.addWidget(save)
        layout.addLayout(actions)

        return page

    def _parse_ints(self, field_text: str) -> list[int]:
        values = []
        for token in field_text.split(","):
            if token.strip():
                values.append(int(token.strip()))
        return values

    def calculate_gate(self) -> None:
        try:
            values = self._parse_ints(self.gate_inputs.text())
            result = gate_truth_table(self.gate_selector.currentText(), values)
            self.gate_result.setPlainText(json.dumps(result, indent=2, default=str))
            self.statusBar().showMessage("Gate calculation complete")
        except Exception as exc:  # pragma: no cover - UI error reporting
            self.gate_result.setPlainText(f"Error: {exc}")
            self.statusBar().showMessage("Gate calculation failed")

    def calculate_compare(self) -> None:
        try:
            result = comparator_math(int(self.signal_input.text()), int(self.threshold_input.text()))
            self.compare_result.setPlainText(json.dumps(result, indent=2, default=str))
            self.statusBar().showMessage("Comparator check complete")
        except Exception as exc:  # pragma: no cover - UI error reporting
            self.compare_result.setPlainText(f"Error: {exc}")
            self.statusBar().showMessage("Comparator check failed")

    def calculate_timing(self) -> None:
        try:
            result = timing_summary(int(self.delay_input.text()), int(self.pulses_input.text()))
            self.timing_result.setPlainText(json.dumps(result, indent=2, default=str))
            self.statusBar().showMessage("Timing analysis complete")
        except Exception as exc:  # pragma: no cover - UI error reporting
            self.timing_result.setPlainText(f"Error: {exc}")
            self.statusBar().showMessage("Timing analysis failed")

    def calculate_farm(self) -> None:
        try:
            result = farm_plan(self.farm_selector.currentText())
            self.farm_result.setPlainText(json.dumps(result, indent=2, default=str))
            self.statusBar().showMessage("Farm plan generated")
        except Exception as exc:  # pragma: no cover - UI error reporting
            self.farm_result.setPlainText(f"Error: {exc}")
            self.statusBar().showMessage("Farm generation failed")

    def _save_json(self, title: str, payload: dict) -> None:
        file_path, _ = QFileDialog.getSaveFileName(self, title, str(Path.home() / "redstone_output.json"), "JSON Files (*.json)")
        if not file_path:
            return
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        self.statusBar().showMessage(f"Saved: {file_path}")

    def export_gate_json(self) -> None:
        try:
            values = self._parse_ints(self.gate_inputs.text())
            self._save_json("Save gate result", gate_truth_table(self.gate_selector.currentText(), values))
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def export_compare_json(self) -> None:
        try:
            self._save_json(
                "Save comparator result",
                comparator_math(int(self.signal_input.text()), int(self.threshold_input.text())),
            )
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def export_timing_json(self) -> None:
        try:
            self._save_json(
                "Save timing result",
                timing_summary(int(self.delay_input.text()), int(self.pulses_input.text())),
            )
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def export_farm_json(self) -> None:
        try:
            self._save_json("Save farm plan", farm_plan(self.farm_selector.currentText()))
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))


def main() -> None:
    app = QApplication([])
    window = RedstonePlannerWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
