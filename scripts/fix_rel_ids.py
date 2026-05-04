import os
import re
import glob

def sanitize(s):
    return s.lower().replace(" ", "_").replace("-", "_")

def fix_relation_ids():
    files = glob.glob("/data/sci-logic-kb/topics/*/papers/*.yaml")
    print(f"Found {len(files)} YAML files to process.")

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Extract author and year from meta section
        author = None
        year = None
        for line in lines:
            # Match: first_author: "Name" or first_author: Name
            amatch = re.search(r"first_author:\s*['\"]?([^'\"\n,]+)['\"]?", line)
            if amatch:
                author = amatch.group(1).strip()
            # Match: year: 2009
            ymatch = re.search(r"year:\s*(\d{4})", line)
            if ymatch:
                year = ymatch.group(1).strip()

        if not author or not year:
            print(f"Could not find author/year in {file_path}, skipping.")
            continue

        prefix = f"rel.{sanitize(author)}_{year}"

        new_lines = []
        for line in lines:
            # Focus on lines that contain 'id: rel.'
            if 'id: rel.' in line:
                # Match 'id: rel.C01' or 'id: "rel.C01"' or 'id: 'rel.C01''
                # Capture the ID part exactly
                match = re.search(r"(id:\s*['\"]?)(rel\.[A-Za-z0-9_.]+)(['\"]?)", line)
                if match:
                    start_part = match.group(1)
                    old_id = match.group(2)
                    end_part = match.group(3)

                    # Extract the unique part (e.g., 'rel.C01' -> '01')
                    # Pattern: rel.[AuthorLetter][Number]
                    if len(old_id) > 5 and old_id[4].isalpha():
                        suffix = old_id[5:] # Keep everything after the first letter
                    elif len(old_id) > 4:
                        suffix = old_id[4:] # Keep everything after 'rel.'
                    else:
                        suffix = "unknown"

                    new_id = f"{prefix}_{suffix}"

                    # Replace only the ID part of the line
                    line = line.replace(old_id, new_id)

            new_lines.append(line)

        if new_lines != lines:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

    print("Finished processing files with aggressive replacement.")

if __name__ == "__main__":
    fix_relation_ids()
