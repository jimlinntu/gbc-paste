from PIL import ImageFont, ImageDraw, Image
import argparse
# https://blog.gtwang.org/programming/opencv-drawing-functions-tutorial/

def paste(name, output):
    image = Image.open("./base.png")
    drawer = ImageDraw.Draw(image)
    name_len = len(name)
    if name_len == 4:
        font = ImageFont.truetype("./標楷體.ttf", 68)
        drawer.text((922, 853), name, font=font, fill=(0, 0, 0))
    elif name_len == 5:
        font = ImageFont.truetype("./標楷體.ttf", 55)
        drawer.text((918, 858), name, font=font, fill=(0, 0, 0))
    elif name_len == 6:
        font = ImageFont.truetype("./標楷體.ttf", 50)
        drawer.text((912, 862), name, font=font, fill=(0, 0, 0))
    else:
        raise NotImplementedError
    image.save(output)

def main(args):
    name = args.name + "同學" if args.student else args.name
    paste(name, args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument("output", type=str)
    parser.add_argument("--student", action="store_true", default=False)
    args = parser.parse_args()
    
    main(args)
