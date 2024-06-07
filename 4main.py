import os
import multiprocessing
import re

def find_file(file):
    with open(file, 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = re.split(r'[.!?,]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    longest_sentence = max(sentences, key=len)
    return longest_sentence

def process_file(file, result):
    longest_sentence = find_file(file)
    result.put((file, longest_sentence))

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    result = multiprocessing.Queue()
    processes = []

    for txt_file in txt_files:
        file = os.path.join(directory, txt_file)
        process = multiprocessing.Process(target=process_file, args=(file, result))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    longest_sentences = []
    while not result.empty():
        longest_sentences.append(result.get())

    for file, longest_sentence in longest_sentences:
        print(f"File nomi: {file}")
        print(f"Eng uzun gap: {longest_sentence}\n")
