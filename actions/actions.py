import json
import os

directory = r"C:/aaTCC/actions"
file_name = "output.json"
file_path = os.path.join(directory, file_name)

with open(file_path, 'r', encoding='utf-8') as f:
    data = f.read()

data = json.loads(data)

# Extrai os dados relevantes
intents = []
responses = []
intent_counts = {}
for obj in data:
    for section in obj['sections']:
        intent_name = section['title']
        if intent_name in intent_counts:
            intent_counts[intent_name] += 1
            intent_name = f"{intent_name}_{intent_counts[intent_name]}"
        else:
            intent_counts[intent_name] = 1
        intents.append(intent_name)
        responses.append(section['content'])

# Cria o arquivo de intents
with open('data/intents2.yml', 'w', encoding='utf-8') as f:
    f.write('intents:\n')  # adiciona a linha "intents:"
    for intent in intents:
        intent_name = intent.replace(" ", "_") # substitui espaços por underline
        f.write(f'  - {intent_name}\n')  # adiciona os intents com a formatação desejada


with open('data/responses2.yml', 'w', encoding='utf-8') as f:
    for i, intent in enumerate(intents):
        intent_name = intent.replace(" ", "_") # substitui espaços por underline
        response = """{}""".format(responses[i].replace('"', '\\"'))  # adiciona aspas triplas e substitui aspas duplas por suas sequências de escape correspondentes
        response = response.replace('\n', '\\n')  # adiciona barra invertida antes de cada quebra de linha
        f.write(f'utter_{intent_name}:\n')
        f.write(f'  - text: "{response}"\n\n')
        
        
