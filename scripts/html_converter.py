#!/usr/bin/env python3
"""
HTML Converter Wrapper

This module provides a simple class-based interface for the HTML conversion
functionality, making it easy to integrate with other applications.
"""

import sys
from pathlib import Path
from typing import List, Optional

# Import the existing HTML conversion classes
try:
    from descriptions_to_html import DescriptionsParser, HTMLGenerator
except ImportError:
    print("Error: Could not import descriptions_to_html module")
    sys.exit(1)


class DescriptionsToHTML:
    """
    Wrapper class for HTML conversion functionality
    """
    
    def __init__(self, title: str = "Image Descriptions"):
        self.title = title
        
    def convert_file(self, input_file: str, output_file: str, 
                    include_details: bool = False) -> bool:
        """
        Convert descriptions file to HTML
        
        Args:
            input_file: Path to input descriptions text file
            output_file: Path to output HTML file
            include_details: Whether to include full metadata details
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            input_path = Path(input_file)
            output_path = Path(output_file)
            
            # Check if input file exists
            if not input_path.exists():
                print(f"Error: Input file '{input_path}' not found")
                return False
            
            # Parse the descriptions file
            parser = DescriptionsParser(input_path)
            entries = parser.parse()
            
            if not entries:
                print("No entries found in the input file")
                return False
            
            # Generate HTML
            generator = HTMLGenerator(entries, self.title, include_details=include_details)
            html_content = generator.generate()
            
            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Successfully generated HTML file: {output_path}")
            print(f"Processed {len(entries)} image descriptions")
            
            return True
            
        except Exception as e:
            print(f"Error during HTML conversion: {e}")
            return False
    
    def get_entry_count(self, input_file: str) -> int:
        """
        Get the number of entries in a descriptions file
        
        Args:
            input_file: Path to input descriptions text file
            
        Returns:
            int: Number of entries, or 0 if file cannot be read
        """
        try:
            input_path = Path(input_file)
            
            if not input_path.exists():
                return 0
                
            parser = DescriptionsParser(input_path)
            entries = parser.parse()
            
            return len(entries)
            
        except Exception:
            return 0
    
    def validate_input_file(self, input_file: str) -> tuple[bool, str]:
        """
        Validate input descriptions file
        
        Args:
            input_file: Path to input descriptions text file
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            input_path = Path(input_file)
            
            if not input_path.exists():
                return False, f"File does not exist: {input_path}"
                
            if not input_path.is_file():
                return False, f"Path is not a file: {input_path}"
                
            if input_path.suffix.lower() != '.txt':
                return False, f"File must be a .txt file: {input_path}"
                
            # Try to parse the file
            parser = DescriptionsParser(input_path)
            entries = parser.parse()
            
            if not entries:
                return False, "No valid entries found in file"
                
            return True, f"Valid file with {len(entries)} entries"
            
        except Exception as e:
            return False, f"Error validating file: {e}"


# For backward compatibility with existing scripts
def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert image descriptions to HTML format"
    )
    
    parser.add_argument(
        "input_file",
        nargs="?",
        default="image_descriptions.txt",
        help="Input descriptions text file (default: image_descriptions.txt)"
    )
    
    parser.add_argument(
        "output_file",
        nargs="?",
        help="Output HTML file (default: input_file with .html extension)"
    )
    
    parser.add_argument(
        "--title",
        default="Image Descriptions",
        help="Title for the HTML page (default: 'Image Descriptions')"
    )
    
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include full metadata details in output"
    )
    
    args = parser.parse_args()
    
    # Set up file paths
    input_file = args.input_file
    output_file = args.output_file
    
    if not output_file:
        # Default output file: replace extension with .html
        output_file = str(Path(input_file).with_suffix('.html'))
    
    # Create converter and convert
    converter = DescriptionsToHTML(args.title)
    success = converter.convert_file(input_file, output_file, args.full)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
