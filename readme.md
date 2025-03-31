# PDF Downloader with Progress and Historisation

A Python tool to download multiple PDF files concurrently with:

- ✅ Per-file download progress bars (with live speed and size)
- ✅ Persistent global progress tracker
- ✅ SSL fallback (tries secure connection first, then unsafe if needed)
- ✅ File size tracking in megabytes
- ✅ Automatic historisation to CSV (timestamp, URL, size)
- ✅ Works in both scripts and Jupyter Notebooks

---

## 📦 Features

- **Multithreaded downloads**: Efficient non-blocking file fetches.
- **SSL fallback**: Secure by default, gracefully handles cert issues.
- **Progress bars**: Visual feedback using `tqdm`.
- **Autosave**: Keeps download history updated every 10 seconds.
- **Notebook-friendly**: Auto-detects and adapts to Jupyter.

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the script

```bash
python downloader.py
```

Download history will be saved in `download_history.csv`.

---

## 📁 Files
```plaintext
pdf-downloader/
├── src/
│   └── downloader.py
├── downloader.py
├── requirements.txt
├── download_history.csv         # auto-generated
├── tests/
│   └── test_downloader.py
└── README.md
```

| File               | Description                                |
|--------------------|--------------------------------------------|
| `downloader.py`    | Main script with logic and threading       |
| `download_history.csv` | Auto-generated log of downloads        |
| `requirements.txt` | List of required Python packages           |

---

## 🧪 Example

```python
pdf_links = [
    "https://example.com/file1.pdf",
    "https://example.com/file2.pdf"
]
```

Each file will be saved as `file_<original_name>.pdf`.

---

## 🧼 Code Quality

- Fully documented functions
- Exception handling for SSL errors
- Modular and testable architecture

### ✅ Sample Test (using pytest)

```python
def test_ssl_fallback():
    from downloader import get_response_with_ssl_fallback
    response = get_response_with_ssl_fallback("https://www.example.com/")
    assert response.status_code == 200
```

---

## 📜 License

MIT License

---

## ✍️ Author
[Emmanuel KOUPOH]()