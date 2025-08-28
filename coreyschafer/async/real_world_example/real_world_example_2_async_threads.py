import asyncio
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


def download_image(url: str, img_num: int) -> Path:
    """
    downloads single image and computes timing
    """
    t1 = time.perf_counter()
    
    ts = int(time.time())
    url = f'{url}?ts={ts}'  # add timestamp for caching issues
    
    response = requests.get(url, timeout=10, allow_redirects=True, stream=True)
    response.raise_for_status()

    # The stream=True parameter ensures memory-efficient downloads.
    filename = f'image_{img_num}.jpg'
    download_path = ORIGINAL_DIR / filename
    print(f"Start downloading {url[:url.find('?')]}")
    with download_path.open('wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    t2 = time.perf_counter()
    print(f'Downloaded url {url[:url.find("?")]} in {download_path} in {t2 - t1:.2f} seconds.')
    return download_path


async def download_images(urls: list[str]) -> list[Path]:
    """
    Download list of images using a single session
    """
    async with asyncio.TaskGroup() as tg:                           # task group
        results = [
            tg.create_task(                                         # task
                asyncio.to_thread(download_image, url, i)           # thread from sync
            )
            for i, url in enumerate(urls, start=1)
        ]
    img_paths = [result.result() for result in results]             # gather results from futures
    return img_paths


def process_single_image(orig_path: Path, max_count: int = 20_000_000) -> Path:
    """
    Simulate a CPU-bound task (like image processing) by running
    a tight loop that performs many calculations.
    Adjust the number to make the task longer or shorter.
    """
    t1 = time.perf_counter()
    save_path = PROCESSED_DIR / orig_path.name
    
    print(f"Start processing {orig_path.name} ({max_count})")
    count = 0
    while count < max_count:
        count += 1
    
    with save_path.open('wb') as f:
        f.write(orig_path.read_bytes())
    
    t2 = time.perf_counter()
    print(f"Finished processing {orig_path.name} ({max_count}), Total time taken: {t2 - t1:.2f} seconds.")
    return save_path


async def process_images(orig_paths: list[Path], max_count: int = 20_000_000) -> list[Path]:
    """
    simulates image processing from a list of paths
    creates task from threads from sync function call
    """
    async with asyncio.TaskGroup() as tg:                           # task group
        results = [
            tg.create_task(                                         # task
                asyncio.to_thread(                                  # thread from sync
                    process_single_image, orig_path, max_count
                )
            )
            for orig_path in orig_paths
        ]
    img_paths = [result.result() for result in results]             # gather results from futures
    return img_paths


async def main():
        
        shutil.rmtree(ORIGINAL_DIR, ignore_errors=True)         # remove data folder
        
        ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)         # create original images data folder
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)        # create processed images data folder
        
        # Run the full synchronous pipeline
        start_time = time.perf_counter()
        print('-------- start downloading images --------')
        downloaded_paths = await download_images(IMAGE_URLS)
        print('-------- end downloading images --------')

        proc_start_time = time.perf_counter()
        print('-------- start processing images --------')
        processed_paths = await process_images(downloaded_paths, 100_000_000)
        print('-------- end processing images --------')

        finish_time = time.perf_counter()
        
        dl_total_time = proc_start_time - start_time
        proc_total_time = finish_time - proc_start_time
        total_time = finish_time - start_time
        
        dl_percent = dl_total_time / total_time * 100
        proc_percent = proc_total_time / total_time * 100
        
        print("\n--- Summary ---")
        print(f"Downloaded {len(downloaded_paths)} images in {dl_total_time:.2f} seconds ({dl_percent:.2f}% of total time.")
        print(f"Processed {len(processed_paths)} images in {proc_total_time:.2f} seconds ({proc_percent:.2f}% of total time.")
        
        """
        --- Summary ---
        Downloaded 12 images in 1.55 seconds (8.96% of total time.
        Processed 12 images in 15.76 seconds (91.04% of total time.
        """


if __name__ == '__main__':
    asyncio.run(main())