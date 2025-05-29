import os
from PIL import Image

def resize_image(input_image_path, output_image_path, desired_width=None, desired_height=None, quality=90, enlarge=False, maintain_aspect_ratio=True):
    """
    Resizes an image to the specified width and/or height.

    Args:
        input_image_path (str): The path to the original image file.
        output_image_path (str): The path where the resized image will be saved.
        desired_width (int, optional): The target width in pixels. If None,
                                        height will be used to calculate width
                                        if maintain_aspect_ratio is True.
        desired_height (int, optional): The target height in pixels. If None,
                                         width will be used to calculate height
                                         if maintain_aspect_ratio is True.
        quality (int, optional): The quality for JPEG images (0-100). Default is 90.
        enlarge (bool, optional): If True, the image will be enlarged if necessary.
                                    Default is False.
        maintain_aspect_ratio (bool, optional): If True, the image's aspect ratio
                                                will be maintained. If False,
                                                the image will be stretched/squashed
                                                to fit the exact desired_width/height.
                                                Default is True.
    Returns:
        bool: True if the image was resized successfully, False otherwise.
    """
    try:
        img = Image.open(input_image_path)
        original_width, original_height = img.size

        if desired_width is None and desired_height is None:
            print("Error: Please provide at least one of 'desired_width' or 'desired_height'.")
            return False

        if maintain_aspect_ratio:
            if desired_width is not None and desired_height is not None:
                # Calculate based on the smaller ratio to ensure it fits within the bounds
                ratio_width = desired_width / original_width
                ratio_height = desired_height / original_height
                scale_factor = min(ratio_width, ratio_height)
                if scale_factor > 1.0 and not enlarge:
                    scale_factor = 1.0
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
            elif desired_width is not None:
                new_width = desired_width
                new_height = int(original_height * (new_width / original_width))
            elif desired_height is not None:
                new_height = desired_height
                new_width = int(original_width * (new_height / original_height))
        else: # Do not maintain aspect ratio, potentially stretch
            new_width = desired_width if desired_width is not None else original_width
            new_height = desired_height if desired_height is not None else original_height

        # Ensure new dimensions are at least 1 pixel
        new_width = max(1, new_width)
        new_height = max(1, new_height)

        resized_img = img.resize((new_width, new_height), Image.LANCZOS) # LANCZOS is a good filter for downsizing

        # Determine the output format based on the extension
        output_format = output_image_path.split('.')[-1].lower()

        if output_format in ['jpeg', 'jpg']:
            resized_img.save(output_image_path, quality=quality, optimize=True)
        else:
            resized_img.save(output_image_path)

        print(f"Image '{input_image_path}' resized to {new_width}x{new_height} and saved as '{output_image_path}'.")
        return True

    except FileNotFoundError:
        print(f"Error: Input image '{input_image_path}' not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    image_directory = './static/images/staging'
    try:
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg')  
        filenames = os.listdir(image_directory)
        for filename in filenames:
            filepath = os.path.join(image_directory, filename)
            # Check if the entry is a file
            if os.path.isfile(filepath) and filename.lower().endswith(image_extensions):
                resize_image(filepath, filepath, desired_width=800, desired_height=800, enlarge=True)
    except FileNotFoundError:
        print(f"Error: Directory '{image_directory}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
    print(f'Program ended')