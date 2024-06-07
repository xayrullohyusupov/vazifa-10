import os
import multiprocessing
import string

def remove_file(file):
    with open(file, 'r', encoding='utf-8') as file:
        text = file.read()
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.translate(translator)
    return clean_text

def process_file(file, result_queue):
    clean_text = remove_file(file)
    result_queue.put((file, clean_text))

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    result_queue = multiprocessing.Queue()
    processes = []

    for txt_file in txt_files:
        file = os.path.join(directory, txt_file)
        process = multiprocessing.Process(target=process_file, args=(file, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    cleaned_texts = []
    while not result_queue.empty():
        cleaned_texts.append(result_queue.get())

    for file_path, clean_text in cleaned_texts:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(clean_text)
        print(f"{file_path} fayli tozalandi")
