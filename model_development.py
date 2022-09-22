import os
import random
import spacy
from spacy.training.example import Example
from spacy.util import minibatch, filter_spans
from thinc.schedules import compounding


# Filters overlapping annotations from a given dataset
def filter_annotations(doc, annotations):
    ents = []
    new_annotations = {"entities": []}
    for start, end, label in annotations["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is not None:
            ents.append(span)
    filtered_ents = filter_spans(ents)
    doc.ents = filtered_ents
    for span in filtered_ents:
        new_annotations["entities"].append([span.start_char, span.end_char, span.label_])
    return doc, new_annotations


# Function utilised to train a new model, if not Model folder is located
def train_model(TRAIN_DATA):
    print("Training model.............")
    nlp = spacy.load('en_core_web_sm')
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    disabled_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    with nlp.disable_pipes(*disabled_pipes):
        optimizer = nlp.create_optimizer()
        for i in range(30):
            random.shuffle(TRAIN_DATA)
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.01, 1.001))
            losses = {}
            for batch in batches:
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    doc, new_annotations = filter_annotations(doc, annotations)
                    example = Example.from_dict(doc, new_annotations)
                    nlp.update([example], drop=0.35, sgd=optimizer, losses=losses)
                print("Losses:", losses)
    if not os.path.isdir("./Model"):
        os.mkdir("Model")
    nlp.to_disk("./Model")
    print("Training complete\n--------------------------------------------------------------------------\n")
    return nlp

