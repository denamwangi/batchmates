summarize_prompt = """
You are programmer with a solid technical foundation. You are extracting structured information from a 
casual introduction. Given the input HTML, extract key data in JSON format that captures the person's:

- name (if stated or inferable)
- current role and/or institution
- technical skills and interests (languages, tools, topics)
- goals at recurse center
- location
- non technical notable hobbies or communities
- anything else

Respond only in JSON like this and do not include any markdown. Keep it concise:

{
  "name": "",
  "role_and_institution": "",
  "technical_skills_and_interests": [],
  "goals": [],
  "location": "",
  "non_technical_hobbies_and_interest": [],
  "other": []
}

"""

condense_list_prompt = """
You are analyzing a list of people’s interests, hobbies, and technical skills to identify shared traits. 
Your job is to normalize and group similar items under standardized tags.

Given a set of items with technical skills, goals, and non-technical hobbies, do the following:

1. Create a set of **standardized tags** (max 45-50).
   - Tags should be lowercase, simple phrases.
   - Merge overlapping concepts (e.g., “graphics programming” + “ray tracing” → “game development” or “computer graphics”)
   - Keep tags high-level but meaningful **except** for rust, and emulators which you should keep specific.
   - Pay attention to what is popular to determine how how level your tags should be

2. Create a mapping from **each original item → its standardized tag**.
   - Do not lose any original items.
   - If an item fits multiple categories, choose the most dominant one.
   - If an item is nonsensical, skip it.

Return two JSON objects with no mardown following the format below exactly:

{
  "standardized_tags": [
    "game development",
    "machine learning",
    "language design",
    "knitting",
    "martial arts",
    "rust",
    ...
  ],
  "mappings": {
    "ray tracing": "computer graphics",
    "Rust": "systems programming",
    "Knitting": "knitting",
    "pico-8": "game development",
    "Taekwondo": "martial arts",
    ...
  }
}
"""