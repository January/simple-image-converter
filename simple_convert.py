import sys
import os

# Try to import Pillow, if it isn't installed, install it
try:
    from PIL import Image
    from PIL import UnidentifiedImageError
except ImportError:
    print("Pillow isn't installed.", end=" ")
    try:
        import pip
        print("We can fix that real quick.")
        pip.main(['install', '--user', "pillow"])
        from PIL import Image
        from PIL import UnidentifiedImageError
    except ImportError:
        print("pip isn't installed either. You'll need to do that before we can proceed.")

args = sys.argv

# Print usage if there's too few args
if len(args) < 3:
    print("Usage: simple_convert.py image1 [image2, image3...] format")
    os._exit(1)

imgs = []
extensions = Image.registered_extensions()
supported_extensions = {e[1:] for e, x in extensions.items()}
file_format = ""

# Iterate over provided arguments to find what's a file and what's our format
for arg in args[1:]:
    try:
        imgs.append(Image.open(arg))
    except FileNotFoundError:
        if arg in supported_extensions:
            file_format = arg
        else:
            print(f"Warning: {arg} doesn't appear to exist. Skipping it.")
    except UnidentifiedImageError:
        print(f"Warning: {arg} isn't an image, or it's one we can't open. Skipping it.")

# Exit if we don't have an actual valid file format
if not file_format:
    print("Error: No valid file format specified! Exiting.")
    os._exit(1)

# Convert the images
for img in imgs:
    try:
        img_filename = img.filename
        new_filename = f"{img_filename.split('.')[0]}.{file_format}"
        print(f"Converting {img_filename} to {new_filename}...", end=" ")
        img.save(new_filename)
        print("Done!")
    # For some reason image format errors are OSErrors
    except OSError as ose:
        if "cannot write mode" in str(ose):
            print("the format you selected doesn't support transparency! Converting and saving anyway. ")
            img = img.convert('RGB')
            img.save(new_filename)
        else:
            print(f"Error, image not converted: {ose}")