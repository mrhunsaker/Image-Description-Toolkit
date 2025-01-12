import os
import subprocess
import sys
from datetime import datetime

def get_image_description(image_path, prompt, log_file):
    """
    Use the Ollama CLI to process an image and get its description.
    """
    try:
        # Log the start time
        start_time = datetime.now()
        with open(log_file, "a") as log:
            log.write(f"Start Time: {start_time}, Image: {image_path}\n")
            log.write(f"Prompt: {prompt}\n")

        # Build the Ollama CLI command
        command = [
            "ollama", "run", "llama3.2-vision"
        ]

        # Start the Ollama process
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Send the custom prompt
        describe_command = f"{prompt} {image_path}\n"
        output, error = process.communicate(describe_command)

        # Log the end time
        end_time = datetime.now()
        with open(log_file, "a") as log:
            log.write(f"End Time: {end_time}, Duration: {end_time - start_time}\n")

        if process.returncode == 0:
            return output.strip()  # The description
        else:
            with open(log_file, "a") as log:
                log.write(f"Error: {error.strip()}\n")
            return f"Error: {error.strip()}"
    except Exception as e:
        with open(log_file, "a") as log:
            log.write(f"Exception: {str(e)}\n")
        return f"Error processing image: {str(e)}"

def process_images_in_directory(directory_path, prompt):
    """
    Loop through images in a directory, save descriptions using Ollama CLI, and generate an HTML file.
    """
    log_file = "processing_log.txt"
    html_file = "image_descriptions.html"

    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    # Start HTML content
    html_content = "<html><head><title>Image Descriptions</title></head><body>"
    html_content += "<h1>Image Descriptions</h1>"

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path) and filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
            print(f"Processing: {filename}")
            description = get_image_description(file_path, prompt, log_file)

            # Save description to a text file with the same name as the image
            text_file_path = os.path.splitext(file_path)[0] + ".txt"
            with open(text_file_path, "w") as text_file:
                text_file.write(description)
            print(f"Description saved to: {text_file_path}")

            # Add description to HTML content
            html_content += f"<h2>{filename}</h2>"
            html_content += f"<p>{description}</p>"

    # Finalize HTML content
    html_content += "</body></html>"

    # Save HTML file
    with open(html_file, "w") as f:
        f.write(html_content)
    print(f"HTML report saved to {html_file}")

def main():
    # Set the default prompt file
    prompt_file = "prompt.txt"

    # Check if a custom prompt file is provided on the command line
    if len(sys.argv) > 1:
        prompt_file = sys.argv[1]

    # Read the prompt from the file
    try:
        with open(prompt_file, "r") as f:
            prompt = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Prompt file '{prompt_file}' not found.")
        return

    directory_path = r"C:\\users\\kelly\\playground\\images"  # Replace with your image directory
    process_images_in_directory(directory_path, prompt)

if __name__ == "__main__":
    main()
