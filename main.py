import os
from xml.etree.ElementTree import ElementTree, Element, iterparse, tostring


def split_large_xml(input_file, output_dir, chunk_size_mb=15):
    """
    Splits a large XML file into smaller files of approximately `chunk_size_mb` size.

    :param input_file: Path to the large input XML file.
    :param output_dir: Directory to save the smaller XML files.
    :param chunk_size_mb: Target size (in MB) of each smaller file.
    """
    os.makedirs(output_dir, exist_ok=True)
    chunk_size_bytes = chunk_size_mb * 1024 * 1024  # Convert MB to bytes

    context = iterparse(input_file, events=("start", "end"))
    _, root = next(context)  # Get the root element
    chunk_index = 1
    current_chunk_size = 0

    # Start with an empty chunk
    chunk_root = Element(root.tag, root.attrib)
    chunk_tree = ElementTree(chunk_root)

    def write_chunk(tree, chunk_idx):
        """Writes the current chunk to a file."""
        chunk_file = os.path.join(output_dir, f"chunk_{chunk_idx:03d}.xml")
        tree.write(chunk_file, encoding="utf-8", xml_declaration=True)
        print(f"Chunk {chunk_idx} written to: {chunk_file}")

    for event, elem in context:
        if event == "end" and elem.tag != root.tag:
            # Append the current element to the chunk root
            chunk_root.append(elem)

            # Calculate the size of the current element
            elem_size = len(tostring(elem, encoding="utf-8"))
            current_chunk_size += elem_size

            # Clear memory for processed element
            elem.clear()

            # Check if the current chunk size exceeds the limit
            if current_chunk_size >= chunk_size_bytes:
                write_chunk(chunk_tree, chunk_index)
                chunk_index += 1
                current_chunk_size = 0

                # Reset the chunk root for the next chunk
                chunk_root = Element(root.tag, root.attrib)
                chunk_tree = ElementTree(chunk_root)

    # Write the last chunk if it has content
    if len(chunk_root) > 0:
        write_chunk(chunk_tree, chunk_index)


# Example usage
if __name__ == "__main__":
    input_file = "books.xml"  # Path to the large input XML file
    output_dir = "output_chunks"  # Directory to store the chunks
    split_large_xml(input_file, output_dir, chunk_size_mb=2)
