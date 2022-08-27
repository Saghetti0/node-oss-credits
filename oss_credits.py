import os
import glob
import json
import datetime

def insensitive_glob_pattern(pattern):
    def either(c):
        return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c
    return "".join(map(either, pattern))

search_dir = "node_modules"
valid_license_patterns = [insensitive_glob_pattern(i) for i in ["license*", "copying*"]]

version = "1.0"

print("Finding all package.json files")

package_jsons = []

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.lower() == "package.json":
            package_jsons.append(os.path.join(root, file))

print(f"Found {len(package_jsons)} package.json files")

name_to_json_data = {}
name_to_license_files = {}

print("Deduplicating packages and getting licenses")

for package_json in package_jsons:
    with open(package_json, "r") as fh:
        try:
            data = json.load(fh)
            if data.get("name") is None:
                continue
            if data["name"] in name_to_json_data:
                continue

            # check for license
            package_path = os.path.dirname(package_json)
            license_files = []
            for pattern in valid_license_patterns:
                glob_result = glob.glob(pattern, root_dir=package_path)
                license_files = [*license_files, *glob_result]

            if len(license_files) < 1:
                continue

            license_files = list(map(lambda x: os.path.join(package_path, x), license_files))

            name_to_json_data[data["name"]] = data
            name_to_license_files[data["name"]] = license_files
        except json.JSONDecodeError as e:
            #print("Malformed JSON in", package_json, "-", e)
            continue

print(f"Filtered down to {len(name_to_json_data)} packages")

print("Generating oss_credits.md")

with open("oss_credits.md", "w") as fh:
    fh.write("# Open source software credits\n")
    fh.write("This software was made possible using the following open-source packages:\n\n")

    for package_name in sorted(name_to_json_data.keys()):
        package_json = name_to_json_data[package_name]
        if package_json.get("homepage"):
            fh.write(f"## [{package_name}]({package_json['homepage']})\n")
        else:
            fh.write(f"## {package_name}\n")
        if package_json.get("description"):
            fh.write(f"{package_json['description']}\n")
        fh.write("\n")
        for license_file in name_to_license_files[package_name]:
            fh.write(f"### `{os.path.basename(license_file)}`\n\n")
            fh.write("```\n")
            with open(license_file, "r") as fh2:
                fh.write(fh2.read().replace("`", "\\`"))
            fh.write("\n```\n")
        fh.write("\n")

    fh.write("\n-----\n")
    fh.write(f"Generated on {datetime.datetime.now().astimezone(datetime.timezone.utc).strftime('%Y-%m-%d at %H:%M:%S UTC')} using [node-oss-credits](https://github.com/Saghetti0/node-oss-credits) {version}\n")

print("Done!")
