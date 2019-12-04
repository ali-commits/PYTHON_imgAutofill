from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json

data = {
    "imagePath": "certificat.png",
    "font": "Prata-Regular.ttf",
    "fontSize": 120,
    "color": [166, 137, 67],
    "xoffset": 10,
    "yoffset": 40,
    "inputFilePath": "input.txt",
    "outputPath": "output",
}


def percent(size):
    return size / 100


def draw_text_center(img, text, fnt, color=(0, 0, 0), xoffset=0, yoffset=0, **kwargs):
    draw = ImageDraw.Draw(img)
    text_size = draw.textsize(text, fnt)
    return draw.text(
        (
            ((img.size[0] - text_size[0]) / 2) + xoffset * percent(img.size[0]),
            yoffset * percent(img.size[1]),
        ),
        text,
        color,
        font=fnt,
        **kwargs,
    )


def fill(img, font, text, data):
    draw_text_center(
        img,
        text,
        font,
        color=tuple(data["color"]),
        xoffset=data["xoffset"],
        yoffset=data["yoffset"],
    )
    return img


def autofill(img, font, data):
    with open(data["inputFilePath"], "r") as f:
        lines = f.readlines()
    i = 0
    for i, line in enumerate(lines):
        imgcopy = img.copy()
        imgcopy = fill(imgcopy, font, line, data)
        imgcopy.save(f'{data["outputPath"]}/{i:0>3}-{line}.png')

        del imgcopy
        print(f'{i+1} images have been generated', end ='\r')

    print(f'{len(lines)} images have been generated')


def main():
#      try execpt to open the configration file (config.json)
#      if the file exesist update the current configration (data)
#      if the file does not exesist then generate a configration file with the default values and save it to (config.json)
    try:
        with open('config.json','r') as f:
            config = json.load(f)
            data.update(config)
        
    except FileNotFoundError:
        print('could not find "config.json" ')
        print('create "config.json" with default values\n')

        with open('config.json','w') as f:
            config = json.dump(data, f, indent=2)

    img = Image.open(data["imagePath"])
    font = ImageFont.truetype(data["font"], 125)

    autofill(img, font, data)

if __name__ == "__main__":
    main()
