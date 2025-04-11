# 📁 Exam Folder Encryption Tool

A simple yet powerful Python GUI application that helps anonymize student exam folders by assigning unique ID codes to each folder. After the grading process, you can safely restore the original folder names with a single click.

---

## 💡 Features

- 🔐 **Encrypt Mode**: Converts student folder names into randomly generated numeric IDs
- 🔁 **Decode Mode**: Automatically detects if folders are encoded and restores their original names
- 📄 **ID Mapping**: Saves a CSV file (`id_map.csv`) containing all folder ↔ ID mappings
- ⚠️ **Safe Rename Handling**: Detects conflicts (like existing folders) and skips them safely
- 🧠 **Unicode Support**: Handles folder names with special or international characters
- 🖼️ **User-Friendly Interface**: Built with Tkinter, featuring confirmation dialogs and feedback

---

## 🛠️ Requirements

No external libraries are required — only built-in Python modules:

- `os`
- `csv`
- `random`
- `tkinter`
- `sys`

---

## 👤 Author

- Created by Muhammad
- Project for Baku Higher Oil School

---

## 🤝 Contributions
Feedback, improvements, or pull requests are always welcome!

---

## 🚀 How to Run

1. Make sure you have **Python 3.x** installed
2. Download or clone this repository
3. Run the script with:

```bash
python "ProjectRename v3(final).py"
