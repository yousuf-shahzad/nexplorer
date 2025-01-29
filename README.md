# Network File Explorer

A PyQt6-based network file explorer application that provides a graphical interface for browsing local and network drives. The application offers features similar to Windows File Explorer but with additional network drive management capabilities.

## Features

- Dual-pane interface with tree view and list view
- Network drive mapping and unmapping functionality
- File filtering and sorting capabilities
- Address bar for direct path navigation
- Back/forward navigation
- Context menu for file operations
- Status bar showing file information
- Support for UNC path navigation
- File and folder filtering options

## Requirements

- Python 3.x
- PyQt6
- Windows Operating System (for network drive mapping features)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/network-file-explorer.git
cd network-file-explorer
```

2. Install required packages:
```bash
pip install PyQt6
```

## Usage

Run the application using Python:
```bash
python main.py
```

### Key Features

1. **Navigation**
   - Use the tree view to browse directories
   - Use the address bar for direct path entry
   - Back/Forward buttons for navigation history

2. **Network Drive Management**
   - Map new network drives with drive letter assignment
   - Unmap existing network drives
   - Automatic detection of mapped network drives

3. **File Operations**
   - Right-click context menu for common operations
   - Open files with default applications
   - Delete and rename capabilities

4. **Filtering and Views**
   - Filter files by type or size
   - Dual-pane view for efficient navigation
   - Detailed file information in status bar

## Code Structure

- `NetworkFileExplorer`: Main application class
- File system model handling with `QFileSystemModel`
- Proxy model for filtering with `QSortFilterProxyModel`
- Network drive management using Windows API through `ctypes`

## Contributing

Contributions are welcome! Please feel free to submit pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for educational and legitimate system administration purposes only. Users are responsible for ensuring they have appropriate permissions for accessing network resources.

## Acknowledgments

- PyQt6 team for the GUI framework
- Contributors to the Python standard library
