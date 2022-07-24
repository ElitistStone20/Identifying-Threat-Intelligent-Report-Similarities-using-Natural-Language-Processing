import random
import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
from Pattern_Matching import construct_entity_set
from pathlib import Path
save_dir = Path("D:\Computer Science\Masters\Dissertation\Project_Code\ThreatReport_Analysis\Model")
# https://www.machinelearningplus.com/nlp/training-custom-ner-model-in-spacy/


def train_ner(TRAIN_DATA):
    print("Training NER model\n--------------------------------------------------------------------------\n")
    nlp = spacy.load('en_core_web_sm')
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    with nlp.disable_pipes(*unaffected_pipes):
        for iteration in range(30):
            # shuffle the examples prior to training
            random.shuffle(TRAIN_DATA)
            losses = {}
            # Batch up the examples using minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    nlp.update(
                        [example],
                        drop=0.4,   # dropout
                        losses=losses
                    )
                    print("Losses: ", losses)
    print("Training complete\n--------------------------------------------------------------------------\n")
    print("Saving model\n--------------------------------------------------------------------------\n")
    nlp.to_disk(save_dir)
    print(f"Model saved to: {save_dir}\n--------------------------------------------------------------------------\n")


def test_ner(TEST_DATA):
    print("Testing NER\n--------------------------------------------------------------------------\n")
    threshhold = 20
    results = []
    nlp_trained = spacy.load(save_dir)
    for text in TEST_DATA:
        doc = nlp_trained(text)
        results.append(
            [(ent.text, ent.label_, text[ent.start:ent.end]) for ent in doc.ents]
        )
    print("Testing complete\n--------------------------------------------------------------------------\n")
    filename = "TestingResults.txt"
    content = ""
    for result in results:
        if len(result) > 0:
            for entity in result:
                if len(entity) > 0:
                    content += f"Entities:\nWord: {entity[0]}\nLabel: {entity[1]}\nSnippet: {entity[2]}\n\n"
    with open(filename, "w") as file:
        file.write(content)
    print(f"Results saved to {filename}\n--------------------------------------------------------------------------\n")


def display_options(TRAIN_DATA, TEST_DATA):
    route = int(input("Enter 1 to train the model or 2 to test the currently trained model"))
    if route == 1:
        train_ner(TRAIN_DATA)
    elif route == 2:
        test_ner(TEST_DATA)
    else:
        display_options()


def main():
    data = construct_entity_set()
    length = len(data)
    TRAIN_DATA = data[0:int(round(length-length/4))]
    TEST_DATA_RAW = data[(length-int(round(length/4))):length]
    TEST_DATA = [document[0] for document in TEST_DATA_RAW]
    display_options(TRAIN_DATA, TEST_DATA)


if __name__ == '__main__':
    main()
