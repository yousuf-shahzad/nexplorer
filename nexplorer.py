import sys
import os
import ctypes
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QListView, QVBoxLayout, QWidget,
    QToolBar, QLineEdit, QStatusBar, QMenu, QMessageBox, QSplitter, QComboBox, QInputDialog, QDialog, QFormLayout, QPushButton
)
from PyQt6.QtGui import QAction, QIcon, QFileSystemModel
from PyQt6.QtCore import Qt, QDir, QSortFilterProxyModel

class NetworkFileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network File Explorer")
        self.setGeometry(100, 100, 1200, 800)

        # Central Widget and Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Back and Forward Buttons
        self.back_action = QAction(QIcon.fromTheme("go-previous"), "Back", self)
        self.forward_action = QAction(QIcon.fromTheme("go-next"), "Forward", self)
        self.toolbar.addAction(self.back_action)
        self.toolbar.addAction(self.forward_action)

        # Address Bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter path or network address...")
        self.address_bar.returnPressed.connect(self.navigate_to_path)
        self.toolbar.addWidget(self.address_bar)

        # Network Drive Selector
        self.network_drive_selector = QComboBox()
        self.network_drive_selector.setPlaceholderText("Select Network Drive")
        self.network_drive_selector.currentIndexChanged.connect(self.on_network_drive_selected)
        self.toolbar.addWidget(self.network_drive_selector)

        # Refresh Button
        self.refresh_action = QAction(QIcon.fromTheme("view-refresh"), "Refresh", self)
        self.refresh_action.triggered.connect(self.refresh_view)
        self.toolbar.addAction(self.refresh_action)

        # Filter Button
        self.filter_action = QAction(QIcon.fromTheme("edit-find"), "Filter", self)
        self.filter_action.triggered.connect(self.show_filter_dialog)
        self.toolbar.addAction(self.filter_action)

        # Splitter for Tree and List Views
        self.splitter = QSplitter()
        self.layout.addWidget(self.splitter)

        # Tree View
        self.tree_view = QTreeView()
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)
        self.splitter.addWidget(self.tree_view)

        # List View
        self.list_view = QListView()
        self.list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)
        self.splitter.addWidget(self.list_view)

        # File System Model
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)

        # Proxy Model for Filtering
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.list_view.setModel(self.proxy_model)

        # Set Root Index
        self.tree_view.setRootIndex(self.model.index(""))
        self.list_view.setRootIndex(self.model.index(""))

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Connect Signals
        self.tree_view.clicked.connect(self.on_tree_view_clicked)
        self.list_view.clicked.connect(self.update_status_bar)

        # Initialize History for Back/Forward
        self.history = []
        self.current_index = -1

        # Detect Network Drives
        self.detect_network_drives()

    def detect_network_drives(self):
        """Detect and populate network drives in the combo box."""
        self.network_drive_selector.clear()
        drives = self.get_network_drives()
        for drive in drives:
            self.network_drive_selector.addItem(f"{drive} ({self.model.filePath(self.model.index(drive))})", drive)

    def get_network_drives(self):
        """Get a list of mapped network drives."""
        drives = []
        for drive_letter in range(ord('A'), ord('Z') + 1):
            drive = f"{chr(drive_letter)}:\\"
            if os.path.exists(drive) and os.path.isdir(drive):
                drives.append(drive)
        return drives

    def on_network_drive_selected(self, index):
        """Handle selection of a network drive from the combo box."""
        if index >= 0:
            drive_path = self.network_drive_selector.itemData(index)
            self.tree_view.setRootIndex(self.model.index(drive_path))
            self.list_view.setRootIndex(self.model.index(drive_path))
            self.address_bar.setText(drive_path)

    def navigate_to_path(self):
        path = self.address_bar.text()
        if os.path.exists(path):
            self.tree_view.setRootIndex(self.model.index(path))
            self.list_view.setRootIndex(self.model.index(path))
            self.update_history(path)
        elif path.startswith("\\\\"):  # UNC Path
            self.tree_view.setRootIndex(self.model.index(path))
            self.list_view.setRootIndex(self.model.index(path))
            self.update_history(path)

    def refresh_view(self):
        current_index = self.tree_view.currentIndex()
        self.tree_view.setRootIndex(self.model.index(""))
        self.tree_view.setCurrentIndex(current_index)
        self.detect_network_drives()  # Refresh network drives

    def on_tree_view_clicked(self, index):
        path = self.model.filePath(index)
        self.list_view.setRootIndex(index)
        self.address_bar.setText(path)
        self.update_status_bar()
        self.update_history(path)

    def update_status_bar(self):
        index = self.list_view.currentIndex()
        if index.isValid():
            file_info = self.model.fileInfo(index)
            self.status_bar.showMessage(f"Selected: {file_info.fileName()} | Size: {file_info.size()} bytes | Modified: {file_info.lastModified().toString()}")

    def show_context_menu(self, position):
        menu = QMenu()
        open_action = menu.addAction("Open")
        delete_action = menu.addAction("Delete")
        rename_action = menu.addAction("Rename")
        action = menu.exec(self.list_view.mapToGlobal(position))

        if action == open_action:
            self.open_file()
        elif action == delete_action:
            self.delete_file()
        elif action == rename_action:
            self.rename_file()

    def open_file(self):
        index = self.list_view.currentIndex()
        if index.isValid():
            file_path = self.model.filePath(index)
            os.startfile(file_path)  # Open file with default application

    def delete_file(self):
        index = self.list_view.currentIndex()
        if index.isValid():
            file_path = self.model.filePath(index)
            confirm = QMessageBox.question(self, "Delete File", f"Are you sure you want to delete {file_path}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                self.model.remove(index)

    def rename_file(self):
        index = self.list_view.currentIndex()
        if index.isValid():
            self.list_view.edit(index)

    def update_history(self, path):
        if self.current_index != len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        self.history.append(path)
        self.current_index += 1

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.navigate_to_path(self.history[self.current_index])

    def go_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.navigate_to_path(self.history[self.current_index])

    def show_filter_dialog(self):
        """Show a dialog to filter files by type or size."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Filter Files")
        layout = QFormLayout(dialog)

        # File Type Filter
        file_type_filter = QLineEdit()
        file_type_filter.setPlaceholderText("e.g., *.txt, *.jpg")
        layout.addRow("File Type Filter:", file_type_filter)

        # File Size Filter
        file_size_filter = QLineEdit()
        file_size_filter.setPlaceholderText("e.g., >1MB, <100KB")
        layout.addRow("File Size Filter:", file_size_filter)

        # Apply Button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.apply_filters(file_type_filter.text(), file_size_filter.text()))
        layout.addRow(apply_button)

        dialog.exec()

    def apply_filters(self, file_type_filter, file_size_filter):
        """Apply filters to the list view."""
        self.proxy_model.setFilterWildcard(file_type_filter)
        # TODO: Add file size filtering logic

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkFileExplorer()
    window.show()
    sys.exit(app.exec())
