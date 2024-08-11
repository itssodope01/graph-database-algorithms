import csv
import gzip
import time
import os
import sys
import io
import contextlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from neo4j.exceptions import TransientError
from utils import get_driver, close_driver, create_unique_constraint, process_batch, create_index
from tqdm import tqdm

class StderrFilter(io.StringIO):
    def write(self, msg):
        if "retried" not in msg:
            sys.__stderr__.write(msg)

@contextlib.contextmanager
def suppress_specific_warnings():
    old_stderr = sys.stderr
    try:
        sys.stderr = StderrFilter()
        yield
    finally:
        sys.stderr = old_stderr

def decompress_file(file_path):
    if file_path.endswith('.gz'):
        decompressed_file_path = file_path[:-3]
        with gzip.open(file_path, 'rb') as f_in, open(decompressed_file_path, 'wb') as f_out:
            total_size = os.path.getsize(file_path)
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Decompressing") as pbar:
                for chunk in iter(lambda: f_in.read(1024 * 1024), b''):
                    f_out.write(chunk)
                    pbar.update(len(chunk))
        return decompressed_file_path
    else:
        return file_path

def read_csv_in_batches(file_path, batch_size=10000):
    batches = []
    with open(file_path, 'r', newline='', encoding='utf-8', buffering=10*1024*1024) as file:
        reader = csv.reader(file, quotechar='"', escapechar='\\', doublequote=False)
        batch = []
        for row in tqdm(reader, desc="Reading rows"):
            if len(row) == 2:
                category, subcategory = row
                batch.append({"category": category, "subcategory": subcategory})
                if len(batch) == batch_size:
                    batches.append(batch)
                    batch = []
        if batch:
            batches.append(batch)
    return batches

def import_batch(batch, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            with suppress_specific_warnings():
                process_batch(batch)
            return len(batch)
        except TransientError:
            retries += 1
            time.sleep((2 ** retries) * 0.5)
    print(f"Failed to process batch after {max_retries} retries: {batch}")
    return 0

def import_data(file_path, batch_size=10000, max_retries=3, num_threads=4):
    start_time = time.time()

    decompressed_file_path = decompress_file(file_path)
    driver = get_driver()

    try:
        with driver.session() as session:
            session.execute_write(create_unique_constraint)
            session.execute_write(create_index)

        batches = read_csv_in_batches(decompressed_file_path, batch_size)

        total_records = 0
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(import_batch, batch, max_retries): batch for batch in batches}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Importing Data to Neo4j"):
                total_records += future.result()

        print(f"Execution completed.\n"
              f"Total Records Created: {total_records}")

        print(f"Importing Data executed in {time.time() - start_time:.4f} seconds.")

    finally:
        close_driver()
        if decompressed_file_path != file_path:
            os.remove(decompressed_file_path)

if __name__ == "__main__":
    import_data("taxonomy_iw.csv.gz")
