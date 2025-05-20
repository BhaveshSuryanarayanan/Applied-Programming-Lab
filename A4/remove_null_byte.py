def remove_null_bytes(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f_in:
        # Read the content of the file
        file_data = f_in.read()

    # Remove null bytes from the content
    cleaned_data = file_data.replace('\x00', '')

    # Write the cleaned data to a new file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write(cleaned_data)

# Example usage
input_file = 'layout.py'
output_file = 'layouts.py'
remove_null_bytes(input_file, output_file)
