import gradio as gr
import hashlib
import os
import random
import string
import csv
from grasshopperAuto import process_grasshopper

def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        hash_obj = hashlib.shake_256()
        hash_obj.update(f.read())
    hash_value = hash_obj.digest(512)

    sizebinary = f"{os.path.getsize(file_path):b}"
    binary_hash_value = sizebinary + ''.join(f"{byte:08b}" for byte in hash_value)

    return binary_hash_value

def generate_random_hash(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def cut_len(lst, length):
    return [lst[i:i + length] for i in range(0, len(lst), length)]

def bin_int(lst):
    return [int(''.join(i), 2) for i in lst]

def pattern_cull_method(lst):
    x_cor = lst[::2]
    y_cor = lst[1::2]
    if len(x_cor) > len(y_cor):
        y_cor.append(x_cor[-1])
    return [x_cor, y_cor]

def process_files(file, inner, outer, height, NodeSize, StrutSize, KinkAngle):
    file_path = file.name
    binary_hash_value = calculate_hash(file_path)
    int_list = bin_int(cut_len(binary_hash_value, 8))
    split_list = pattern_cull_method(int_list)

    # Prepare the coordinates for process_grasshopper
    CorX = split_list[0]
    CorY = [counter * 4 for counter in range(len(split_list[0]))]  # Assuming a step of 4
    CorZ = split_list[1]

    # Generate a unique file name using a random hash
    random_hash = generate_random_hash()
    output_file_name = f"output_{random_hash}.3dm"
    output_file_path = os.path.join("./output", output_file_name)

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    output_Cor_name = f"output_{"Fix"}.csv"
    output_Cor_path = os.path.join("./output", output_Cor_name)
    with open(output_Cor_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for x, y, z in zip(CorX, CorY, CorZ):
            writer.writerow([x, y, z])  # Writing the data
        print("File written successfully.")

    # Call the grasshopper processing function with the new definition
    process_grasshopper(CorX, CorY, CorZ, output_file_path, inner, outer, height, NodeSize, StrutSize, KinkAngle)

    return output_file_path  # Return the path of the output file for download

iface = gr.Interface(
    fn=process_files,
    inputs=[
        gr.File(label="Select a file"),
        gr.Slider(0.00, 0.20, value=0.026, step=0.001, label="Inner"),
        gr.Slider(0.00, 0.20, value=0.101, step=0.001, label="Outer"),
        gr.Slider(0.00, 0.20, value=0.068, step=0.001, label="Height"),
        gr.Slider(0.00, 1, value=0.508, step=0.001, label="NodeSize"),
        gr.Slider(0.00, 10, value=5.196, step=0.001, label="StrutSize"),
        gr.Slider(0.00, 1.3, value=0.717, step=0.001, label="KinkAngle")
    ],
    outputs=gr.File(label="Download Output File"),
    title="Grasshopper File Processor",
    description="Upload a file to process with Grasshopper and tune the parameters."
)

if __name__ == '__main__':
    iface.launch()
