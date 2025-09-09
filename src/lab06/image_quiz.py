import base64
from glob import glob


def base64encode_image(image_file):
    with open(file=image_file, mode='rb') as f:
        data = f.read()
        return base64.b64encode(data).decode(encoding='utf-8')


def main():
    for g in glob('./images/*.jpg'):
        encoded = base64encode_image(g)
        print(encoded[:100])


if __name__ == '__main__':
    main()
