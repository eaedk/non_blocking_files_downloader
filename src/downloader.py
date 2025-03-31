"""
PDF Downloader with Progress and Historisation

Features:
- Concurrent downloads using threads
- SSL fallback: tries verify=True, then verify=False
- Progress bars for individual files and overall progress
- File size in MB
- Periodic autosave to CSV
- Compatible with Jupyter and scripts
"""

import pandas as pd
from datetime import datetime, UTC
import requests
from threading import Thread, Lock
import time
from queue import Queue
import sys, os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Suppress warning if needed


# Environment-aware progress bar
if 'ipykernel' in sys.modules:
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm

# Globals
history = pd.DataFrame(columns=['timestamp_utc', 'url', 'file_size_mb'])
history_lock = Lock()
autosave_interval = 10  # seconds
download_done_queue = Queue()


def get_response_with_ssl_fallback(url: str) -> requests.Response:
    """Attempt HTTPS request with SSL verification fallback."""
    try:
        return requests.get(url, stream=True, verify=True)
    except requests.exceptions.SSLError:
        return requests.get(url, stream=True, verify=False)


def download_and_log(url: str, path: str):
    """Download a file, show progress, log metadata."""
    response = get_response_with_ssl_fallback(url)
    total_size = int(response.headers.get('content-length', 0))
    chunk_size = 8192
    size_bytes = 0

    progress = tqdm(
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc=path,
        leave=False,
        position=1
    )

    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                size_bytes += len(chunk)
                progress.update(len(chunk))

    progress.close()

    size_mb = round(size_bytes / (1024 * 1024), 2)
    with history_lock:
        history.loc[len(history)] = [datetime.now(UTC), url, size_mb]

    download_done_queue.put(1)


def start_download_thread(url: str, path: str) -> Thread:
    """Start a threaded download."""
    thread = Thread(target=download_and_log, args=(url, path))
    thread.start()
    return thread


def autosave_history(file_path: str):
    """Periodically save history to CSV."""
    while True:
        time.sleep(autosave_interval)
        with history_lock:
            history.to_csv(file_path, index=False)


if __name__ == '__main__':

        # Download path setup
    __basefile_dir__ = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(__basefile_dir__, "..", "Downloads", "pdf")
    os.makedirs(download_path, exist_ok=True)
    history_file = os.path.join(download_path, 'download_history.csv')

    # Start autosave thread
    Thread(target=autosave_history, args=(history_file,), daemon=True).start()

    # List of files to download
    pdf_links = [
        "https://www.brvm.org/sites/default/files/20230918_-_rapport_dactivites_du_1er_trimestre_2023_-_boa_sn.pdf",
        "https://www.brvm.org/sites/default/files/rapport_dactivite_2nd_semestre_2022_-_boa_senegal.pdf",
        "https://www.brvm.org/sites/default/files/20230310_-_etats_financiers_certifies_2022_-_boa_sn.pdf",
        "https://www.brvm.org/sites/default/files/20221207_-_rapport_dactivite_3e_trimestre_2022_-_boa_senegal.pdf",
        "https://www.brvm.org/sites/default/files/20221116_-_rapport_dactivite_-_1er_semestre_2022_-_boa_senegal.pdf"
    ]
    

    # Start downloads
    for link in pdf_links:
        filename = os.path.join(download_path, f'file_{link.split("/")[-1]}')
        start_download_thread(link, filename)

    # Persistent overall progress bar
    with tqdm(total=len(pdf_links), desc='Files downloaded', unit='file', position=0) as overall:
        while overall.n < overall.total:
            download_done_queue.get()
            overall.update(1)

    # Save the history
    history.to_csv(history_file, index=False)