import os
import multiprocessing

def count_file(file):
    with open(file, 'r', encoding='utf-8') as file:
        text = file.read()
    words = text.split()
    return len(words)

def process_file(file_path, result_queue):
    word_count = count_file(file_path)
    result_queue.put(word_count)

if __name__ == "__main__":
    directory = "C:\\Users\\Lord Name\\Desktop\\10-dars"
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

    words = 0
    while not result_queue.empty():
        words += result_queue.get()

    print(f"Umumiy so'zlar soni: {words}")
