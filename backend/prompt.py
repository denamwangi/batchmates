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
You are analyzing a list of people's interests, hobbies, and technical skills to identify shared traits. 
Your job is to normalize and group similar items under standardized tags, with a strong emphasis on technical topics.

Given a set of items with technical skills, goals, and non-technical hobbies, do the following:

1. Create a set of **standardized tags** (max 45-50).
   - Tags should be lowercase, simple phrases.
   - **Prioritize technical granularity**: ~80% of tags should be technical/skills-based, ~20% non-technical hobbies.
   - For technical items:
     * Keep specificity where there's meaningful clustering (e.g., separate "machine learning", "computer graphics", "systems programming")
     * Merge only when concepts truly overlap (e.g., "react" + "vue" + "angular" → "frontend frameworks")
     * Preserve niche technical interests that appear multiple times (e.g., "rust", "emulators", "compilers")
   - For non-technical items:
     * Group more aggressively into broad categories (e.g., "soccer" + "basketball" + "running" → "sports")
     * Only create separate tags for non-technical interests if they appear frequently
   - Balance granularity with popularity: if 10+ people mention a specific technical area, give it its own tag

2. Create a mapping from **each original item → its standardized tag**.
   - Do not lose any original items.
   - If an item fits multiple categories, choose the most dominant/specific one.
   - If an item is nonsensical, skip it.

Return two JSON objects with no markdown following the format below exactly:

{
  "standardized_tags": [
    "machine learning",
    "computer graphics",
    "systems programming",
    "web development",
    "rust",
    "emulators",
    "compilers",
    "sports",
    "music",
    ...
  ],
  "mappings": {
    "ray tracing": "computer graphics",
    "Rust": "rust",
    "React development": "web development",
    "Knitting": "crafts",
    "soccer": "sports",
    "pico-8": "game development",
    "Taekwondo": "martial arts",
    ...
  }
}
"""


# condense_list_prompt = """
# You are analyzing a list of people’s interests, hobbies, and technical skills to identify shared traits. 
# Your job is to normalize and group similar items under standardized tags.

# Given a set of items with technical skills, goals, and non-technical hobbies, do the following:

# 1. Create a set of **standardized tags** (max 45-50).
#    - Tags should be lowercase, simple phrases.
#    - Merge overlapping concepts (e.g., “graphics programming” + “ray tracing” → “game development” or “computer graphics”)
#    - Keep tags high-level but meaningful **except** for rust, and emulators which you should keep specific.
#    - Pay attention to what is popular to determine how how level your tags should be

# 2. Create a mapping from **each original item → its standardized tag**.
#    - Do not lose any original items.
#    - If an item fits multiple categories, choose the most dominant one.
#    - If an item is nonsensical, skip it.

# Return two JSON objects with no markdown following the format below exactly:

# {
#   "standardized_tags": [
#     "game development",
#     "machine learning",
#     "language design",
#     "knitting",
#     "martial arts",
#     "rust",
#     ...
#   ],
#   "mappings": {
#     "ray tracing": "computer graphics",
#     "Rust": "systems programming",
#     "Knitting": "knitting",
#     "pico-8": "game development",
#     "Taekwondo": "martial arts",
#     ...
#   }
# }
# """