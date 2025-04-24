import concurrent.futures

import flammkuchen as fl
import os
import numpy as np
import time
import string
import random
import shutil

import concurrent.futures


def generate_and_save_file(file_path, size=1024 * 1024):
    """Generate a file with random content and save it to the given path.

    Args:
    - file_path: Path to save the file.
    - size: Size of the file in bytes. Default is 1MB.
    """
    # Generate random data
    content = ''.join(random.choices(string.ascii_letters + string.digits, k=size))

    # Save the file
    with open(file_path, 'w') as file:
        file.write(content)


if __name__ == "__main__":

    path = "txt_files"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    
    num_files = 50  # Number of files to create
    file_paths = [f"{path}/file_{i}.txt" for i in range(num_files)]

    start = time.time()
    for path in file_paths:
        generate_and_save_file(path)
    end = time.time()

    print("----------------------------")
    print(f"Single thread: {end - start}")
    print("----------------------------")

    # delete files
    for f in file_paths:
        os.remove(f)

    # Multithreading
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(generate_and_save_file, file_paths)
    end = time.time()
    print(f"Multithreading time: {end - start}")
    print("----------------------------")