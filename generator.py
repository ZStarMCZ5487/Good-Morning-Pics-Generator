import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import tkinter as tk
import random

#image_url_hmm = random.randint(1, 2)
#if image_url_hmm == 1:
#    image_url = "https://api.waifu.pics/sfw/waifu"
#else:
#    image_url = give me husbando version... pls 👉👈🥺

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All required packages installed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

install_requirements()


root = tk.Tk()
root.title("Good Morning Pics Generator")
root.geometry("400x300")

def generate():

    image_url = "https://api.waifu.pics/sfw/waifu"

    response = requests.get(image_url)

    if response.status_code == 200:
        data = response.json()
        image_response = requests.get(data["url"])
        img = Image.open(BytesIO(image_response.content))
    else:
        print("Failed to fetch image")
        exit()

    draw = ImageDraw.Draw(img)
    width, height = img.size

    if selected_lang.get() == "English":
        with open("title/title_en.txt", "r", encoding="utf-8") as file:
            title = file.readlines()
        title = [line.strip() for line in title if line.strip()]
        random_title = random.choice(title)
        title_size = width/10
        wrapped_title= textwrap.fill(random_title, width=10)

        with open("description/description_en.txt", "r", encoding="utf-8") as file:
            description = file.readlines()
        description = [line.strip() for line in description if line.strip()]
        random_description = random.choice(description)
        description_size = width/12
        wrapped_description = textwrap.fill(random_description, width=20)

    elif selected_lang.get() == "Chinese":
        with open("title/title_cn.txt", "r", encoding="utf-8") as file:
            title = file.readlines()
        title = [line.strip() for line in title if line.strip()]
        random_title = random.choice(title)
        title_size = width/6
        wrapped_title= textwrap.fill(random_title, width=2)

        with open("description/description_cn.txt", "r", encoding="utf-8") as file:
            description = file.readlines()
        description = [line.strip() for line in description if line.strip()]
        random_description = random.choice(description)
        description_size = width/15
        wrapped_description= textwrap.fill(random_description, width=10)

    title_font = ImageFont.truetype("ttf/NotoSansSC-Medium.ttf", size=title_size)
    description_font = ImageFont.truetype("ttf/NotoSansSC-Medium.ttf", size=description_size)

    title_pos_hmm = random.randint(0,1)
    if title_pos_hmm == 1:
        title_position = (width/2 - 50, 50)
    else:
        title_position = (50, 50)

    R = random.randint(0, 255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)
    text_color = (R, G, B)

    color = random.randint(0, 255)
    outline_color = (color, color, color)

    for offset_x in [-2, 0, 2]:
        for offset_y in [-2, 0, 2]:
            draw.text((title_position[0] + offset_x, title_position[1] + offset_y),
                      wrapped_title, font=title_font, fill=outline_color)


    draw.text(title_position, wrapped_title, fill=text_color, font=title_font)

    description_position = (10, height/3*2)

    for offset_x in [-2, 0, 2]:
        for offset_y in [-2, 0, 2]:
            draw.multiline_text((description_position[0] + offset_x, description_position[1] + offset_y),
                      wrapped_description, font=description_font, fill=outline_color)

    draw.multiline_text(description_position, wrapped_description, fill=text_color, font=description_font)

    img.show()
    img.save("output.png")

label = tk.Label(root, text="Choose a language:", font=("Arial", 14))
label.pack(pady=10)


lang = ["English", "Chinese"]

selected_lang = tk.StringVar()
selected_lang.set(lang[0])

dropdown = tk.OptionMenu(root, selected_lang, *lang)
dropdown.config(font=("Arial", 12))
dropdown.pack(pady=10)

button = tk.Button(root, text="Generate", font=("Arial", 14), command=generate)
button.pack(pady=10)

root.mainloop()