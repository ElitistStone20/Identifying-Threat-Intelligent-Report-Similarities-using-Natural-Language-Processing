# Pattern matching entities of interest with their labels
import os
import re

labels = [
    ["charming kitten", "CYBER_GROUP"],
    ["ghostwriter", "CYBER_GROUP"],
    ["unc1151", "CYBER_GROUP"],
    ["turla", "CYBER_GROUP"],
    ["confucius", "CYBER_GROUP"],
    ["patchwork", "CYBER_GROUP"],
    ["oceanlotus", "CYBER_GROUP"],
    ["lazarus", "CYBER_GROUP"],
    ["apt28", "CYBER_GROUP"],
    ["silverfish", "CYBER_GROUP"],
    ["fancy bear", "CYBER_GROUP"],
    ["wiper", "MALWARE"],
    ["viper", "MALWARE"],
    ["dustman", "MALWARE"],
    ["loki", "MALWARE"],
    ["keylogger", "ATTACK"],
    ["spyware", "MALWARE"],
    ["simjacker", "ATTACK"],
    ["sim jacker", "ATTACK"],
    ["backdoor", "ATTACK"],
    ["phishing", "ATTACK"],
    ["ransomeware", "RANSOMWARE"],
    ["snake", "RANSOMWARE"],
    ["jpcertcc", "ORGANISATION"],
    ["mandiant", "ORGANISATION"],
    ["clearsky", "ORGANISATION"],
    ["blink", "ORGANISATION"],
    ["apt", "THREAT_ACTOR"],
    ["advanced persistent threat", "THREAT_ACTOR"],
    ["moonknight maze", "THREAT_ACTOR"],
    ["bitdefender", "ANTIVIRUS"],
    ["mcafee", "ANTIVIRUS"],
    ["ahnlab", "ANTIVIRUS"]
]


def load_data():
    path_of_the_directory = 'D:\Computer Science\Masters\Dissertation\Project_Code\ThreatReport_Analysis\Data\TextFiles'
    data = []
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory, filename)
        if os.path.isfile(f):
            with open(f, "r", encoding='utf-8') as file:
                data.append(file.read())
    return data


def construct_entity_set():
    data = load_data()
    entity_list = []
    for document in data:
        entities = []
        for entity in labels:
            location = re.finditer(rf'\b({entity[0]})\b', document)
            for m in location:
                entities.append((m.start(), m.end(), entity[1]))
        entity_list.append((document, {"entities": entities}))
    return entity_list
