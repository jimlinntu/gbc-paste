from PIL import ImageFont, ImageDraw, Image
import argparse
# https://blog.gtwang.org/programming/opencv-drawing-functions-tutorial/
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument("output", type=str)
    parser.add_argument("--student", action="store_true", default=False)
    args = parser.parse_args()
    image = Image.open("./base.png")
    font = ImageFont.truetype("./標楷體.ttf", 55)
    drawer = ImageDraw.Draw(image)
    name = args.name + "同學" if args.student else args.name
    drawer.text((918, 858), name, font=font, fill=(0, 0, 0))
    image.save(args.output)

if __name__ == "__main__":
    
    main()
