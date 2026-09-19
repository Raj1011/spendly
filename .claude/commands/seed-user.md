---
description: Create a single dummy user in the database
allowed tools: Read, Bash(python3:*)
---

Read database/db.py to understand the users table schema and get_db() helper.

Then write and run a Python script using Bash that:

1. Generates a realsitic random Indian user using Your own knowledge of common Indian names across regions:
    - Name: a realistic indian first + lastname
    - Email: derive from the name with a random 2-3 digit number suffix (e.g: rahul.sharma91@gmail.com)
    - Password: "password123" hashed with werzeug's generate_passsword_hash
    - created_at: current datetime

2. Check if the generated email already exists in the users table. If it does, regenerate until unique.

3. Insert the user into the database using the same get_db() pattern found in db.py.

4. Print confirmation:
    - id
    - name
    - email