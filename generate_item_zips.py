#!/usr/bin/env python3
import os
import json
import zipfile

# === CONFIGURE THESE PATHS ===
# Directory containing the two source files:
INPUT_DIR  = "/storage/emulated/0/0API Tools/tool"
# Output directory for per-ID JSON files
OUTPUT_DIR = "item_jsons"
# Name of the final ZIP archive
ZIP_NAME   = "items.zip"
# =============================

# Only process these two filenames:
SOURCE_FILES = [
    "ob46_added_itemData.json",
    "ob47_added_itemData.json",
]

def load_items(input_dir, filenames):
    items = []
    for fn in filenames:
        path = os.path.join(input_dir, fn)
        print(f"→ Loading {path}")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise RuntimeError(f"Expected an array in {fn}, got {type(data).__name__}")
        items.extend(data)
    print(f"Loaded {len(items)} total items")
    return items

def write_per_id(items, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for itm in items:
        item_id = itm.get("itemID")
        desc    = itm.get("description", "")
        if not item_id:
            continue
        out_path = os.path.join(out_dir, f"{item_id}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            # write the bare description string as JSON
            json.dump(desc, f, ensure_ascii=False)
        count += 1
    print(f"Wrote {count} files into ./{out_dir}/")

def make_zip_folder(source_dir, zip_name):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for fn in os.listdir(source_dir):
            full = os.path.join(source_dir, fn)
            zf.write(full, arcname=fn)
    print(f"Packaged files into ./{zip_name}")

def main():
    items = load_items(INPUT_DIR, SOURCE_FILES)
    write_per_id(items, OUTPUT_DIR)
    make_zip_folder(OUTPUT_DIR, ZIP_NAME)

if __name__ == "__main__":
    main()