import xml.etree.ElementTree as ET
import os


def split_xml(input_file, output_dir, chunk_size=1):
    """
    Splits a large XML file into smaller chunks based on size and selects only the first 235 elements (columns) from each row.

    Args:
        input_file: Path to the input XML file.
        output_dir: Directory to store the output chunks.
        chunk_size: Maximum size of each chunk in megabytes (default: 1 MB).
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        chunk_bytes = chunk_size * 1024 * 1024
        chunk_number = 1
        current_chunk_size = 0
        current_chunk = ET.Element("root")
        output_file = os.path.join(output_dir, f"chunk_{chunk_number}.xml")

        context = ET.iterparse(input_file, events=("start", "end"))
        _, root = next(context)

        for event, elem in context:
            if event == "end" and elem.tag != root.tag:
                # Select only the first 235 child elements (if applicable)
                trimmed_elem = ET.Element(elem.tag, attrib=elem.attrib)
                trimmed_elem.extend(list(elem)[:235])  # Keep only the first 235 child elements

                element_size = len(ET.tostring(trimmed_elem, encoding="utf-8"))

                if current_chunk_size + element_size > chunk_bytes:
                    tree = ET.ElementTree(current_chunk)
                    tree.write(output_file, encoding="utf-8", xml_declaration=True)
                    print(f"Chunk created as chunk_{chunk_number}.xml")

                    current_chunk = ET.Element("root")
                    current_chunk_size = 0
                    chunk_number += 1
                    output_file = os.path.join(output_dir, f"chunk_{chunk_number}.xml")

                current_chunk.append(trimmed_elem)
                current_chunk_size += element_size

                root.clear()

        if len(current_chunk):
            tree = ET.ElementTree(current_chunk)
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            print(f"Chunk created as chunk_{chunk_number}.xml")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the input file exists and the output directory is accessible.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    input_file = "books.xml"  # Path to your large XML file
    output_dir = "xml_chunks"  # Directory to save the chunks
    split_xml(input_file, output_dir, chunk_size=1)  # Chunk size set to 1 MB
