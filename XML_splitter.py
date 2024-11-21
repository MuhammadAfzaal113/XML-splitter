import xml.etree.ElementTree as ET
import os


def split_xml(input_file, output_dir, chunk_size=15):
    """
    Splits a large XML file into smaller chunks based on size.

    Args:
        input_file: Path to the input XML file.
        output_dir: Directory to store the output chunks.
        chunk_size: Maximum size of each chunk in bytes (default: 15 MB).
    """

    try:
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        chunk_bytes = chunk_size * 1024 * 1024
        tree = ET.parse(input_file)
        root = tree.getroot()

        current_chunk = ET.ElementTree(ET.Element(root.tag))
        current_chunk_size = 0

        chunk_number = 1
        output_file = os.path.join(output_dir, f"chunk_{chunk_number}.xml")

        for child in root:
            child_size = len(ET.tostring(child))
            if current_chunk_size + child_size > chunk_bytes:
                print('Chunk created as chunk_' + str(chunk_number) + '.xml')

                current_chunk.write(output_file)
                current_chunk = ET.ElementTree(ET.Element(root.tag))
                current_chunk_size = 0
                chunk_number += 1
                output_file = os.path.join(output_dir, f"chunk_{chunk_number}.xml")

            current_chunk.getroot().append(child)
            current_chunk_size += child_size

        # Write the last chunk
        current_chunk.write(output_file)
        print('Chunk created as chunk_' + str(chunk_number) + '.xml')

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the input file exists and the output directory is accessible.")


if __name__ == '__main__':
    input_file = "books.xml"
    output_dir = "xml_chunks"
    split_xml(input_file, output_dir, chunk_size=15)
