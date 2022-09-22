from Tree import json_to_tree, distance


# Calculates the similarity between documents using an input label
def calculate_similarity_label(doc1, doc2, tree, label):
    ent_distances = []
    for ent1 in doc1.ents:
        for ent2 in doc2.ents:
            if ent1.label_ == ent2.label_:
                if ent1.label_.lower() == label:
                    ent_distances.append((tree, distance(tree, ent1, ent2)))
    percentages = []
    for distance_ in ent_distances:
        percentages.append((distance_[1] / distance_[0].max_distance))
    total = 0
    for percentage in percentages:
        total += percentage
    if tree.max_distance > 0:
        ret = (total / tree.max_distance) * 100
        return ret
    return 0


# Calculates the similarity between documents when no label was provided
def calculate_similarity(doc1, doc2, alias_tree, company_tree, attack_tree):
    ent_distances = []
    trees_used = []
    total_percent = 0
    for ent1 in doc1.ents:
        for ent2 in doc2.ents:
            if ent1.label_ == ent2.label_:
                if ent1.label_.lower() == "cyber_alias":
                    ent_distances.append((alias_tree, distance(alias_tree, ent1, ent2)))
                    total_percent += alias_tree.max_distance
                    if alias_tree not in trees_used:
                        trees_used.append(alias_tree)
                elif ent1.label_.lower() == "company":
                    ent_distances.append((company_tree, distance(company_tree, ent1, ent2)))
                    total_percent += company_tree.max_distance
                    if company_tree not in trees_used:
                        trees_used.append(company_tree)
                else:
                    ent_distances.append((attack_tree, distance(attack_tree, ent1, ent2)))
                    total_percent += attack_tree.max_distance
                    if attack_tree not in trees_used:
                        trees_used.append(attack_tree)
    percentages = []
    for distance_ in ent_distances:
        percentages.append((distance_[1] / distance_[0].max_distance) * 100)
    total = 0
    for percentage in percentages:
        total += percentage
    if total_percent > 0:
        ret = round((total / total_percent) * 100, 4)
        return ret
    return 0


# Main similarity method called which dictates which calculation function above is utilised
def custom_similarity(other_docs, doc, other_filenames, doc_filename, alias_tree, company_tree, attack_tree, label=None):
    document_distances = []
    if label is None:
        i = 0
        for doc1 in other_docs:
            sim = calculate_similarity(doc, doc1, alias_tree, company_tree, attack_tree)
            document_distances.append((doc_filename, other_filenames[i], sim))
            i += 1
    else:
        tree = json_to_tree(label.lower(), other_docs)
        i = 0
        for doc1 in other_docs:
            sim = calculate_similarity_label(doc, doc1, tree, label)
            document_distances.append((doc_filename, other_filenames[i], sim))
            i += 1
    document_distances = sorted(document_distances, key=lambda tup: tup[2], reverse=True)
    return document_distances[0]
