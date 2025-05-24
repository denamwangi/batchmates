import zulip
import os
import csv
import json
from openai import OpenAI
from prompt import summarize_prompt, condense_list_prompt
import random


ZULIP_SECRET = os.environ.get('ZULIP_SECRET')
INTROS_CSV_FILE_NAME = 'zulip_intros2.csv'
INTROS_JSON_FILE_NAME = 'zulip_intros_json.json'
CONDENSED_LIST_FILE_NAME = 'condensed_list.json'
zulip_client = zulip.Client(api_key=ZULIP_SECRET, email='dena.mwangi@gmail.com', site='https://recurse.zulipchat.com')
openai_client = OpenAI()
MODEL = 'o4-mini-2025-04-16'



def get_zulip_data():
    # subscriptions = zulip_client.get_subscriptions()

    request = {
        "anchor": "newest",
        "num_before": 100,
        "num_after": 0,
        "narrow": [
            {"operator": "channel", "operand": "👋 welcome!"},
            {"operator": "topic", "operand": "introductions for Summer 1, 2025"}
        ]
    }
    result = zulip_client.get_messages(request)
    return result

def save_zulip_data(data):
    with open(INTROS_CSV_FILE_NAME, 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "content"])
        for msg in data:
            name = msg["sender_full_name"]
            content = msg['content']
            if len(content) > 600:
                writer.writerow([name, content])


def save_intro_json(name, structured_intro):
    if os.path.exists(INTROS_JSON_FILE_NAME):
        with open(INTROS_JSON_FILE_NAME, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    print(' ')
    # print(data)
    data[name] = structured_intro

    with open(INTROS_JSON_FILE_NAME, 'w') as f:
        json.dump(data, f, indent=2)

def call_llm(intro, prompt):
    response = openai_client.chat.completions.create(
        model=MODEL,
        messages=[{
            "role": "developer",
            "content": f" {prompt}"
        }, 
        {
            "role": "user",
            "content": f"Here is the info: {intro}"
        }]
    )
    content = response.choices[0].message.content
    # print(content)
    return content
    

def get_llm_structured_output():
    with open(INTROS_CSV_FILE_NAME, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            structured_output = call_llm(row, summarize_prompt)
            structured_output_json = json.loads(structured_output)
            id = random.random()
            save_intro_json(structured_output_json.get('name', f'nameless_{id}'), structured_output_json)
            # import pdb; pdb.set_trace()

fields =['non_technical_hobbies_and_interest', 'technical_skills_and_interests']
# fields =['other','non_technical_hobbies_and_interest', 'role_and_institution', 'technical_skills_and_interests','goals','location']
def combine_all_interests():
    interests = set()
    with open(INTROS_JSON_FILE_NAME, 'r') as f:
        data = json.load(f)

        for _, info in data.items():
            for field in fields:

                interests.update(info[field])
    print(interests)
    return interests

def get_llm_condensed_output():
    raw_interests = combine_all_interests()

    response = call_llm(raw_interests, condense_list_prompt)
    print(response)
    response_json = json.loads(response)

    with open('condensed_list3.json', 'w') as f:
        json.dump(response_json, f, indent=2)
    # import pdb; pdb.set_trace()


fields =['other','non_technical_hobbies_and_interest', 'role_and_institution', 'technical_skills_and_interests','goals']

def build_nodes():
    nodes = []
    links = []
    person_to_interest = {}
    with open(CONDENSED_LIST_FILE_NAME, 'r') as condensed_file:
        condensed_tags = json.load(condensed_file)
        standardized_tags = condensed_tags['standardized_tags']
        mappings = condensed_tags['mappings']

        for tag in standardized_tags:
            nodes.append({
                'id': tag,
                'type': "interest"
            })
    with open(INTROS_JSON_FILE_NAME, 'r') as f:
        intros = json.load(f)
        no_mapping = set()
        for name, info in intros.items():
            nodes.append({
                'id': name,
                'type': 'person'  
            })
            person_to_interest[name] = set()
            for field in fields:
                # print(f" \n {info[field]}, len: {type(info[field])}")
                
                if type(info[field]) == list:
                    for item in info[field]:
                        # print(f"{item}  maps to {mappings.get(item)}")
                        normalized_interest = mappings.get(item)
                        if normalized_interest: 
                            person_to_interest[name].add(normalized_interest)
                        else:
                            no_mapping.add(item)
    seen = set()
    people = [person for person in person_to_interest]
    for i in range(len(people)-1):
        for j in range(len(people)-1):
            person1 = people[i]
            person2 = people[j]
            pairing = person1+person2 
            pairing2 = person2+person1

            skip = pairing in seen or pairing2 in seen
            print(seen)
            print(f" \n {person1} and {person2}-> skip? {skip}")
            commonalities = ', '.join(person_to_interest[person1].intersection(person_to_interest[person2]))
            if person1 != person2 and len(commonalities) > 0 and not skip:
                links.append({
                    "source": person1,
                    "target": person2,
                    "label": commonalities
                })
                seen.add(pairing)
                seen.add(pairing2)
    # print(nodes)
    print(links, len(links))


intro_data = {
    "name": "Robbie",
    "role": "Assistant Professor",
    "institution": "Rutgers–Newark",
    "technical_skills": ["Rust", "Lua", "Zig"],
    "creative_interests": ["music"],
    "learning_interests": ["Japanese"],
    "projects": [
        { "title": "hither", "description": "forth-like toy language" },
        { "title": "form-of-danger", "description": "game jam game" },
        { "title": "seamstress", "description": "Lua environment" }
    ],
    "location": "Brooklyn",
    "open_to_collab": "yes",
    "other": ["comp sci prof", "math background"]
}

if __name__ == "__main__":
    # data = get_zulip_data()
    # messages = data['messages']
    # import pdb; pdb.set_trace()
    # save_zulip_data(messages)
    
    # save_intro_json('Robbie',intro_data )
    # get_llm_structured_output()
    # get_llm_condensed_output()
    # build_nodes()
    get_llm_condensed_output()