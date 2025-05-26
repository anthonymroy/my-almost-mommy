import os
import uuid

def main():
    image_directory = './static/images/staging'
    try:
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg')  
        old_filenames = os.listdir(image_directory)
        for old_filename in old_filenames:
            old_filepath = os.path.join(image_directory, old_filename)
            # Check if the entry is a file
            if os.path.isfile(old_filepath) and old_filename.lower().endswith(image_extensions):
                _, extension = os.path.splitext(old_filepath)
                new_filename = str(uuid.uuid4())+extension
                new_filepath = os.path.join(image_directory, new_filename)
                os.rename(old_filepath, new_filepath)
    except FileNotFoundError:
        print(f"Error: Directory '{image_directory}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
    print(f'Program ended')