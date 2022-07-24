import string
import nltk
from collections import Counter
from nltk.corpus import stopwords
import os
import matplotlib.pyplot as plt


def load_data():
    path_of_the_directory = 'D:\Computer Science\Masters\Dissertation\Project_Code\ThreatReport_Analysis\Data\TextFiles'
    data = []
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory, filename)
        if os.path.isfile(f):
            with open(f, "r", encoding='utf-8') as file:
                data.append(file.read())
    return data


def remove_stopwords(data):
    new_data = []
    punct = set(string.punctuation)
    stop_words = set(stopwords.words('english'))
    for document in data:
        filtered_data = [word for word in document.split() if word not in stop_words and word not in punct]
        new_data.append(' '.join(filtered_data))
    return new_data


def word_frequency(data):
    def add_to_frequencies(document_frequencies):
        for frequency in document_frequencies:
            for i in range(0, len(frequencies)):
                if frequency[0] == frequencies[i][0]:
                    frequencies[i] = (frequencies[i][0], frequencies[i][1] + frequency[1])
                    return
            frequencies.append(frequency)

    frequencies = []
    for document in data:
        add_to_frequencies(Counter(document.split()).most_common(10))
    return sorted(frequencies, key=lambda tup: tup[1], reverse=True)


def plot_frequencies(frequencies):
    for freq in frequencies:
        print(f"{freq}\n")
    xAxis = []
    yAxis = []
    for freq in frequencies:
        xAxis.append(freq[0])
        yAxis.append(freq[1])
    plt.plot(xAxis, yAxis)
    plt.title("Word Frequencies")
    plt.xlabel("Words")
    plt.ylabel("Occurrences")
    plt.show()


def main():
    data = remove_stopwords(load_data())
    frequencies = word_frequency(data)
    qrt = int(round(len(frequencies)/4))
    plot_frequencies(frequencies)


if __name__ == '__main__':
    main()
