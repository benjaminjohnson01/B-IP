from PIL import Image

# write a python program that can take multiple specified images and combine them into a single image, either side-by-side or stacked vertically. allow for a specified working directory and output directory. allow for the input of white, black, or transparent space to be placed between each image in either configuration. add a setting that allows for each image to be trimmed by a specified number of pixels on either the sides or the top and bottom prior to merging. add a setting that can remove the background of each image prior to merging.

def combine_images(images, output_path, mode='horizontal', spacing=0, spacing_color='transparent', no_background=False):

    def remove_background(image):
        background_color = (255, 255, 255)  # Assuming white background
        threshold = 0  # Adjust this value to control the sensitivity of background removal
        rgba_image = image.convert('RGBA')
        pixels = rgba_image.getdata()
        new_pixels = []
        for pixel in pixels:
            if abs(pixel[0] - background_color[0]) <= threshold and abs(pixel[1] - background_color[1]) <= threshold and abs(pixel[2] - background_color[2]) <= threshold:
                new_pixels.append((pixel[0], pixel[1], pixel[2], 0))
            else:
                new_pixels.append(pixel)
        rgba_image.putdata(new_pixels)
        return rgba_image

    # Open the first image to get the size
    first_image = Image.open(images[0])
    width, height = first_image.size

    # Calculate the size of the combined image
    if mode == 'horizontal':
        combined_width = width * len(images) + spacing * (len(images) - 1)
        combined_height = height
    elif mode == 'vertical':
        combined_width = width
        combined_height = height * len(images) + spacing * (len(images) - 1)
    else:
        raise ValueError("Invalid mode. Must be 'horizontal' or 'vertical'.")

    # Create a new blank image with the calculated size and spacing color
    if spacing_color == 'transparent':
        combined_image = Image.new('RGBA', (combined_width, combined_height))
    else:
        combined_image = Image.new('RGB', (combined_width, combined_height), spacing_color)

    # Paste each image onto the combined image with the specified spacing
    x = 0
    y = 0
    for image_path in images:
        image = Image.open(image_path)

        # Remove the background if no_background is True
        if no_background:
            image = remove_background(image)

        combined_image.paste(image, (x, y))
        if mode == 'horizontal':
            x += width + spacing
        elif mode == 'vertical':
            y += height + spacing

    # Save the combined image to the output path
    combined_image.save(output_path)

# Usage
image_1 = 'C:\\Users\\benjo\\iCloudDrive\\Desktop\\Spring 2024\\ME 601 - Metal Additive Manufacturing\\Tibia\\Images\\TibiaR003-isometric-cropped.png'
image_2 = 'C:\\Users\\benjo\\iCloudDrive\\Desktop\\Spring 2024\\ME 601 - Metal Additive Manufacturing\\Tibia\\Images\\TibiaR003-front-cropped.png'
image_3 = 'C:\\Users\\benjo\\iCloudDrive\\Desktop\\Spring 2024\\ME 601 - Metal Additive Manufacturing\\Tibia\\Images\\TibiaR003-right-cropped.png'
images = [image_1, image_2, image_3]
output_path = 'C:\\Users\\benjo\\Downloads\\output.png'

mode = 'horizontal'  # 'horizontal' or 'vertical'
spacing = 100  # spacing between images in pixels
spacing_color = 'white'  # 'white' or 'black' or 'transparent'
no_background = False  # True or False

combine_images(images, output_path, mode, spacing, spacing_color, no_background)