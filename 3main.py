import os
import multiprocessing
import re

def count_file(file):
    with open(file, 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)

def process_file(file, result_queue):
    sentence_count = count_file(file)
    result_queue.put(sentence_count)

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    result_queue = multiprocessing.Queue()
    processes = []

    for txt_file in txt_files:
        file_path = os.path.join(directory, txt_file)
        process = multiprocessing.Process(target=process_file, args=(file_path, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total = 0
    while not result_queue.empty():
        total += result_queue.get()

    print(f"Umumiy gaplar soni: {total}")
