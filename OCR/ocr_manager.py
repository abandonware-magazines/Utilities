#!/usr/bin/env python3

#from queue import Queue
from pathlib import Path
from functools import partial
from collections import namedtuple
from unittest.mock import patch, Mock
from multiprocessing.dummy import Pool as ThreadPool

import multiprocessing
import magazine_db
import argparse
import logging
import ocr
import os


OCRResult = namedtuple("OCRResult", "path text")
Magazine = namedtuple("Magazine", "magazine_name issue_num page_num")

FORMAT = "[%(threadName)s, %(asctime)s, %(levelname)s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

NUM_THREADS = 5

def get_files(base_folder, extension):
    for path in Path(base_folder).rglob(f'*.{extension}'):
        yield(path)

def perform_ocr(input_queue, output_queue):
    while not input_queue.empty():
        path = input_queue.get()
        output = ocr.perform_ocr(path, heuristic_autocorrect = True)
        output_queue.put(OCRResult(path, output))

def path_to_magazine_details(path):
    path = os.path.normpath(path)
    path_arr = path.split(os.sep)
    magazine_name = path_arr[-3]
    issue_num = int(path_arr[-2])
    file_name_arr = os.path.splitext(path_arr[-1])
    page_num = int(file_name_arr[0])
    return Magazine(magazine_name, issue_num, page_num)

def process_text(mag_db, input_queue, output_queue):
    while True:
        ocr_result = input_queue.get()
        if ocr_result is None:
            return

        logging.info("Processing text for '{}' ".format(ocr_result.path))
        #print(ocr_result.text)
        magazine_details = path_to_magazine_details(ocr_result.path)
        mag_db.add_text(magazine_details.magazine_name, magazine_details.issue_num, magazine_details.page_num, ocr_result.text)
        logging.info("Done processing text for '{}' ".format(ocr_result.path))
        output_queue.put(ocr_result.path)

def main(base_folder, progress_db_path):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), progress_db_path), "a+", buffering = 1) as progress_db:
        img_queue  = multiprocessing.Queue()
        text_queue = multiprocessing.Queue()
        done_queue = multiprocessing.Queue()

        mag_db = magazine_db.MagazineDB()

        progress_db.seek(0)
        done_files = set(progress_db.read().splitlines())

        num_images = 0
        for img_file in get_files(base_folder, "jpg"):
            if str(img_file) not in done_files:
                num_images += 1
                img_queue.put(img_file)
            else:
                logging.info(f"Skipping '{img_file}' since already done")

        logging.info(f"Added {num_images} images to queue")

        process_pool = multiprocessing.Pool(multiprocessing.cpu_count(), perform_ocr, (img_queue, text_queue))
        process_pool.close()

        thread_pool = ThreadPool(NUM_THREADS, process_text, (mag_db, text_queue, done_queue))
        
    
        while num_images > 0:
            logging.info(f"Waiting for done jobs, number of jobs left: {num_images}")
            result = done_queue.get()
            progress_db.write("{}\n".format(result))
            logging.info(f"Done with {result} ")
            num_images -= 1
    
        for _ in range(NUM_THREADS):
            text_queue.put(None)

        logging.debug(f"Closing thread pool")
        thread_pool.close()

        logging.debug(f"Waiting for processes")
        process_pool.join()

        logging.debug(f"Waiting for threads")
        thread_pool.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Magazine OCR Manager')
    parser.add_argument('-p', '--path', action='store', required = True, help='Path to folder with magazine scans')
    parser.add_argument('-d', '--debug', action = 'store_true', default = False, help = 'Debug mode: Simulate OCR and DB access')
    args = parser.parse_args()

    progress_db_path = "done.txt"

    if args.debug:

        ocr.perform_ocr = Mock(return_value="dummy_text")
        magazine_db.MagazineDB = Mock()
        progress_db_path = "done_debug.txt"

    main(args.path, progress_db_path)