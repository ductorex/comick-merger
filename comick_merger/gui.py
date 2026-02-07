"""PyQt6 GUI for comick-merger."""

import sys
from pathlib import Path
from typing import List, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel, QFileDialog,
    QMessageBox, QRadioButton, QButtonGroup, QProgressBar,
    QAbstractItemView, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

from comick_merger.cbz_merger import CBZMerger


class MergeWorker(QThread):
    """Worker thread for merging CBZ files."""

    progress = pyqtSignal(str)  # Progress message
    finished = pyqtSignal(bool, str)  # Success, message

    def __init__(self, cbz_paths: List[Path], output_path: Path, use_prefixes: bool):
        super().__init__()
        self.cbz_paths = cbz_paths
        self.output_path = output_path
        self.use_prefixes = use_prefixes

    def run(self):
        """Run the merge operation."""
        try:
            self.progress.emit("Loading CBZ files...")
            merger = CBZMerger(self.cbz_paths)

            self.progress.emit("Detecting conflicts...")
            conflicts = merger.detect_conflicts()

            if conflicts:
                method = "prefixes" if self.use_prefixes else "folders"
                self.progress.emit(
                    f"Found {len(conflicts)} conflicts, resolving with {method}..."
                )

            self.progress.emit("Merging files...")
            merger.merge(self.output_path, use_prefixes=self.use_prefixes)

            self.progress.emit("Done!")
            self.finished.emit(True, f"Successfully merged {len(self.cbz_paths)} CBZ files!")

        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class CBZListWidget(QListWidget):
    """Custom list widget that accepts drag & drop of CBZ files."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Accept drag events with files."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        """Accept drag move events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event: QDropEvent):
        """Handle dropped files."""
        if event.mimeData().hasUrls():
            cbz_files = []
            for url in event.mimeData().urls():
                path = Path(url.toLocalFile())
                if path.suffix.lower() in ['.cbz', '.zip']:
                    cbz_files.append(path)

            if cbz_files:
                # Use window() to get MainWindow regardless of reparenting
                main_window = self.window()
                if hasattr(main_window, 'add_cbz_files'):
                    main_window.add_cbz_files(cbz_files)

            event.acceptProposedAction()
        else:
            super().dropEvent(event)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.cbz_paths: List[Path] = []
        self.output_path: Optional[Path] = None
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Comick Merger")
        self.setMinimumSize(800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("CBZ Merger")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(title_label)

        # Splitter for list and log
        splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(splitter, 1)

        # Top section: file list
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # File list section
        list_label = QLabel("CBZ Files (drag to reorder):")
        top_layout.addWidget(list_label)

        self.file_list = CBZListWidget(self)
        top_layout.addWidget(self.file_list, 1)

        # Buttons for file management
        button_layout = QHBoxLayout()

        self.add_files_btn = QPushButton("Add Files...")
        self.add_files_btn.clicked.connect(self.add_files)
        button_layout.addWidget(self.add_files_btn)

        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()
        top_layout.addLayout(button_layout)

        splitter.addWidget(top_widget)

        # Bottom section: log
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        log_label = QLabel("Log:")
        bottom_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        bottom_layout.addWidget(self.log_text)

        splitter.addWidget(bottom_widget)

        # Output section
        output_layout = QHBoxLayout()
        output_label = QLabel("Output file:")
        output_layout.addWidget(output_label)

        self.output_line = QLabel("(not selected)")
        self.output_line.setStyleSheet("padding: 5px; border: 1px solid #ccc; background: #f5f5f5;")
        output_layout.addWidget(self.output_line, 1)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.browse_btn)

        main_layout.addLayout(output_layout)

        # Conflict resolution options
        options_layout = QHBoxLayout()
        options_label = QLabel("Conflict resolution:")
        options_layout.addWidget(options_label)

        self.method_group = QButtonGroup()

        self.prefix_radio = QRadioButton("Prefixes (0_file.jpg)")
        self.prefix_radio.setChecked(True)
        self.method_group.addButton(self.prefix_radio)
        options_layout.addWidget(self.prefix_radio)

        self.folder_radio = QRadioButton("Folders (0/file.jpg)")
        self.method_group.addButton(self.folder_radio)
        options_layout.addWidget(self.folder_radio)

        options_layout.addStretch()
        main_layout.addLayout(options_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Merge button
        self.merge_btn = QPushButton("Merge CBZ Files")
        self.merge_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.merge_btn.clicked.connect(self.merge_files)
        self.merge_btn.setEnabled(False)
        main_layout.addWidget(self.merge_btn)

        self.log("Ready. Add CBZ files to begin.")

    def log(self, message: str):
        """Add a message to the log."""
        self.log_text.append(message)

    def add_files(self):
        """Open file dialog to add CBZ files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select CBZ Files",
            "",
            "CBZ Files (*.cbz *.zip);;All Files (*)"
        )

        if files:
            cbz_paths = [Path(f) for f in files]
            self.add_cbz_files(cbz_paths)

    def _display_name(self, path: Path) -> str:
        """Return a display name, adding parent dir if names conflict."""
        names = [p.name for p in self.cbz_paths]
        if names.count(path.name) > 1:
            return f"{path.parent.name}/{path.name}"
        return path.name

    def _refresh_display_names(self):
        """Refresh all item labels to reflect current duplicate state."""
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            path = Path(item.data(Qt.ItemDataRole.UserRole))
            item.setText(self._display_name(path))

    def add_cbz_files(self, paths: List[Path]):
        """Add CBZ files to the list."""
        for path in paths:
            if path not in self.cbz_paths:
                self.cbz_paths.append(path)
                item = QListWidgetItem(path.name)
                item.setData(Qt.ItemDataRole.UserRole, str(path))
                self.file_list.addItem(item)
                self.log(f"Added: {path.name}")
        self._refresh_display_names()

        self.update_merge_button()

    def remove_selected(self):
        """Remove selected files from the list."""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            row = self.file_list.row(item)
            self.file_list.takeItem(row)
            removed_path = self.cbz_paths.pop(row)
            self.log(f"Removed: {removed_path.name}")

        self._refresh_display_names()
        self.update_merge_button()

    def clear_all(self):
        """Clear all files from the list."""
        if not self.cbz_paths:
            return

        reply = QMessageBox.question(
            self,
            "Clear All",
            "Remove all files from the list?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.file_list.clear()
            self.cbz_paths.clear()
            self.log("Cleared all files.")
            self.update_merge_button()

    def browse_output(self):
        """Browse for output file location."""
        file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Merged CBZ As",
            "merged.cbz",
            "CBZ Files (*.cbz);;All Files (*)"
        )

        if file:
            self.output_path = Path(file)
            self.output_line.setText(str(self.output_path))
            self.log(f"Output: {self.output_path.name}")
            self.update_merge_button()

    def update_merge_button(self):
        """Enable/disable merge button based on state."""
        can_merge = len(self.cbz_paths) >= 2 and self.output_path is not None
        self.merge_btn.setEnabled(can_merge)

    def merge_files(self):
        """Start the merge operation."""
        if len(self.cbz_paths) < 2:
            QMessageBox.warning(self, "Error", "Need at least 2 CBZ files to merge.")
            return

        if not self.output_path:
            QMessageBox.warning(self, "Error", "Please select an output file.")
            return

        # Disable UI during merge
        self.merge_btn.setEnabled(False)
        self.add_files_btn.setEnabled(False)
        self.remove_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(0)  # Indeterminate progress

        # Get current order from list (using stored path data)
        current_paths = []
        for i in range(self.file_list.count()):
            path = Path(self.file_list.item(i).data(Qt.ItemDataRole.UserRole))
            current_paths.append(path)

        # Start worker thread
        use_prefixes = self.prefix_radio.isChecked()
        self.worker = MergeWorker(current_paths, self.output_path, use_prefixes)
        self.worker.progress.connect(self.log)
        self.worker.finished.connect(self.merge_finished)
        self.worker.start()

    def merge_finished(self, success: bool, message: str):
        """Handle merge completion."""
        self.progress_bar.setVisible(False)
        self.add_files_btn.setEnabled(True)
        self.remove_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.update_merge_button()

        if success:
            QMessageBox.information(self, "Success", message)
            self.log(message)
        else:
            QMessageBox.critical(self, "Error", message)
            self.log(f"ERROR: {message}")


def main():
    """Main entry point for the GUI."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
