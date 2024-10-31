#Author         TheStair
#Assignment     Project3
#Class          Comp5350

#Personal Statement
#I Certify that this code is solely my own, and/or when I utilize external sources it is clearly cited.


#Project Goal
#Extract files from a supplied disk image using file signatures.

import os
import sys
import hashlib
import struct

#Define File Signature variables
#Sourced from www.garykessler.net/library/file_sigs.html

#I originally planned to utilize defined variables, but after consideration, a dictionary is a better
# way to structure the file signatures

# I used the internet to figure out how to define byte literals in python. (the \x)

#Dictionary Structure, 'fileType': (file start signature, EOF marker)
file_signatures = {
    'pdf': (b'\x25\x50\x44\x46',b'\x25\x25\x45\x4f\x46'),
    'gif': (b'\x47\x49\x46\x38', b'\x00\x3b'),
    'jpg': (b'\xff\xd8\xff', b'\xff\xd9'),
    'png': (b'\x89\x50\x4e\x47', b'\x49\x45\x4e\x44\xae\x42\x60\x82'),
    'avi': (b'\x52\x49\x46\x46', b'\x00\x00') #Placeholder, AVI file size is 4 bytes LE after sig
}

def calculate_sha256(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    return sha256_hash.hexdigest()

def carve_files(disk_image, signatures):
    with open(disk_image, 'rb') as f:
        data = f.read()

    output_folder = "recovered_files"
    os.makedirs(output_folder, exist_ok=True)

    disk_length = len(data)
    recovered_files = []

    # Iterate through the dictionary for each file type
    for file_type, (start_sig, end_sig) in signatures.items():
        start_pos = 0

        # Loop while the start position exists within the disk image
        while start_pos < disk_length:
            # Find the first instance of the start signature
            start_pos = data.find(start_sig, start_pos)

            # If the start position exists within the disk
            if start_pos != -1:
                # print("Searching for Filetype: " + file_type)

                # File end position temporarily held just after the signature
                end_pos = start_pos + len(start_sig)

                # AVI files lack an EOF marker, so they are different
                if file_type == 'avi':
                    # File size bytes immediately follow the starting signature
                    file_size_pos = start_pos + len(start_sig)

                    # If the file size string exists in the disk image
                    if file_size_pos + 4 <= disk_length:
                        # Pull the 4 bytes of LE File size and convert them from LE
                        file_size_bytes = data[file_size_pos:file_size_pos + 4]
                        file_size = struct.unpack('<I', file_size_bytes)[0]

                        # End position is file size + header
                        end_pos = start_pos + 8 + file_size

                        # Ensure that the end position exists in the file
                        if end_pos <= disk_length:
                            file_data = data[start_pos:end_pos]
                            file_hash = calculate_sha256(file_data)

                            #store files in a dictionary to be referenced later
                            recovered_files.append({
                                "type": file_type,
                                "start_offset": start_pos,
                                "end_offset": end_pos,
                                "data": file_data,
                                "hash": file_hash
                            })
                            start_pos = end_pos  # Move start_pos to end of current file to continue searching
                        else:
                            print(file_type + " end position out of range")
                            break
                    else:
                        print(file_type + " start position out of range")
                        break

                # For other file types with an end signature
                else:
                    # print("found " + file_type + " file")
                    end_pos = data.find(end_sig, start_pos)
                    if end_pos != -1:
                        if end_pos != start_pos+ len(start_sig):
                            end_pos += len(end_sig)  # Include the EOF signature in the file
                            file_data = data[start_pos:end_pos]
                            file_hash = calculate_sha256(file_data)

                            # store files in a dictionary to be referenced later
                            recovered_files.append({
                                "type": file_type,
                                "start_offset": start_pos,
                                "end_offset": end_pos,
                                "data": file_data,
                                "hash": file_hash
                            })
                        start_pos = end_pos  # Move start_pos to end of current file to continue searching
                    else:
                        print(f"{file_type} end signature not found after start at {start_pos}")
                        start_pos += len(start_sig)  # Increment start_pos to avoid infinite loop

            else:
                #print("Did not find any" + file_type + " files")
                break  # Exit loop if start signature is not found

    # Display recovered file information
    print("The disk image contains " + str(len(recovered_files)) + " files")
    index = 1
    for file in recovered_files:
        file_path = os.path.join(output_folder, f"recovered_{index}.{file['type'].lower()}")
        with open(file_path, "wb") as out_file:
            out_file.write(file['data'])
        index += 1
        print(f"Saved recovered_file{index}.{file['type']}, Start Offset {hex(file['start_offset'])}"
              f", End Offset {hex(file['end_offset'])} \n SHA-256: {file['hash']}")

    print(f"\nRecovered Files are located in {os.path.abspath(output_folder)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter a disk image to analyze.")
        sys.exit(1)

    #disk_image = "Project3.dd"
    #carve_files(disk_image, file_signatures)
    carve_files(sys.argv[1], file_signatures)


