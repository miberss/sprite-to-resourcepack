import os
import json
from PIL import Image

def generate_resource_pack_sk(input_folder, resource_pack_folder):
    """Generates the resource_pack.sk file and places it in the resource pack folder."""
    resource_pack_sk = "on script load:\n"
    
    resource_pack_sk_path = os.path.join(resource_pack_folder, "resource_pack.sk")
    if os.path.exists(resource_pack_sk_path):
        with open(resource_pack_sk_path, "r", encoding="utf-8") as file:
            resource_pack_sk = file.read()
    for index, filename in enumerate(sorted(os.listdir(input_folder))):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            char = chr(0xE000 + index)
            if f"loadSprite(\"{char}\",\"{filename}\")" not in resource_pack_sk:
                resource_pack_sk += f"  loadSprite(\"{char}\",\"{filename}\")\n"
    with open(resource_pack_sk_path, "w", encoding="utf-8") as file:
        file.write(resource_pack_sk)
    
    print(f"resource_pack.sk file updated at {resource_pack_sk_path}")

def update_font_json(input_folder, resource_pack_folder):
    """Updates the font JSON file with new sprite entries."""
    font_json_path = os.path.join(resource_pack_folder, "assets", "minecraft", "font", "default.json")
    providers = []
    if os.path.exists(font_json_path):
        with open(font_json_path, "r", encoding="utf-8") as font_file:
            font_data = json.load(font_file)
            providers = font_data.get("providers", [])

    for index, filename in enumerate(sorted(os.listdir(input_folder))):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            char = chr(0xE000 + index)
            new_provider = {
                "type": "bitmap", "file": f"minecraft:sprites/{filename}", "ascent": 9, "height": 12, "chars": [char]
            }
            if new_provider not in providers:
                providers.append(new_provider)
    font_data = {"providers": providers}
    with open(font_json_path, "w", encoding="utf-8") as font_file:
        json.dump(font_data, font_file, separators=(',', ':'))
    
    print(f"font/default.json file updated at {font_json_path}")

version_to_pack_format = {
    "1.20": 15,
    "1.20.1": 15,
    "1.20.2": 18,
    "1.20.3": 22,
    "1.20.4": 22,
    "1.20.5": 32,
    "1.20.6": 32,
    "1.21": 34,
    "1.21.1": 34,
    "1.21.2": 42,
    "1.21.3": 42,
    "1.21.4": 46,
    "1.21.4-pre1": 46,
}

def get_pack_format(version):
    """Returns the pack_format for a given Minecraft version."""
    return version_to_pack_format.get(version)

minecraft_version = input("What version is your Minecraft (e.g., 1.20.1)? ").strip()
pack_name = input("Enter the name of your resource pack: ").strip()
pack_description = input("Enter a description for your resource pack: ").strip()
input_folder = input("Enter the input folder path (for images): ").strip()
output_folder = input("Enter the output folder path for the resource pack: ").strip()

main_folder = os.path.join(output_folder, pack_name)
os.makedirs(main_folder, exist_ok=True)
assets_folder = os.path.join(main_folder, "assets", "minecraft")
font_folder = os.path.join(assets_folder, "font")
textures_folder = os.path.join(assets_folder, "textures", "sprites")
os.makedirs(font_folder, exist_ok=True)
os.makedirs(textures_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(textures_folder, filename)
        with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
            f_out.write(f_in.read())

mcmeta_path = os.path.join(main_folder, "pack.mcmeta")
mcmeta_content = {
    "pack": {
        "pack_format": get_pack_format(minecraft_version),
        "description": pack_description
    }
}
with open(mcmeta_path, "w", encoding="utf-8") as mcmeta_file:
    json.dump(mcmeta_content, mcmeta_file, indent=2)

generate_resource_pack_sk(input_folder, main_folder)
update_font_json(input_folder, main_folder)
print(f"Resource pack '{pack_name}' created/updated successfully at {main_folder}!")