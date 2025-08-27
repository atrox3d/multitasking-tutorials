import re
import shutil
import time
from pathlib import Path

import requests

IMAGE_URLS = [
    "https://images.unsplash.com/photo-1516117172878-fd2c41f4a759?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1532009324734-20a7a5813719?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1524429656589-6633a470097c?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1530224264768-7ff8c1789d79?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1564135624576-c5c88640f235?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1541698444083-023c97d3f4b6?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1522364723953-452d3431c267?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1516972810927-80185027ca84?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1550439062-609e1531270e?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=1920&h=1080&fit=crop",
]

ORIGINAL_DIR = Path('data/original_images')
PROCESSED_DIR = Path('data/processed_images')


def download_image(session: requests.Session, url: str, img_num: int) -> Path:
    ts = int(time.time())
    url = f'{url}?ts={ts}'  # add timestamp for caching issues
    print(f'Downloading url {url}...')
    
    response = session.get(url, timeout=10, allow_redirects=True, stream=True)
    response.raise_for_status()

    # The stream=True parameter ensures memory-efficient downloads.
    filename = f'image_{img_num}.jpg'
    download_path = ORIGINAL_DIR / filename
    
    with download_path.open('wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f'Downloaded in {download_path}')
    return download_path


def download_images(urls: list[str]) -> list[Path]:
    with requests.Session() as session:
        image_paths = [
            download_image(session, url, i)
            for i, url in enumerate(urls, start=1)
        ]
        
    return image_paths


def process_single_image(orig_path: Path, max_count: int = 20_000_000) -> Path:
    print(f"Processing {orig_path.name}, {max_count = }...")
    t1 = time.perf_counter()
    save_path = PROCESSED_DIR / orig_path.name
    
    # Simulate a CPU-bound task (like image processing) by running
    # a tight loop that performs many calculations.
    # Adjust the number to make the task longer or shorter.
    count = 0
    while count < max_count:
        count += 1
    
    with save_path.open('wb') as f:
        f.write(orig_path.read_bytes())
    
    t2 = time.perf_counter()
    print(f"Finished processing {orig_path.name}, Total time taken: {t2 - t1:.2f} seconds.")
    return save_path


def process_images(orig_paths: list[Path], max_count: int = 20_000_000) -> list[Path]:
    img_paths = [process_single_image(orig_path, max_count) for orig_path in orig_paths]
    return img_paths


if __name__ == '__main__':
    t1 = time.perf_counter()
    
    shutil.rmtree(ORIGINAL_DIR, ignore_errors=True)
    
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run the full synchronous pipeline
    downloaded_paths = download_images(IMAGE_URLS)
    processed_paths = process_images(downloaded_paths, 100_000_000)

    t2 = time.perf_counter()

    print("\n--- Summary ---")
    print(f"Downloaded {len(downloaded_paths)} images.")
    print(f"Processed {len(processed_paths)} images.")
    print(f"Total time taken: {t2 - t1:.2f} seconds")
