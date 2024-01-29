import hashlib
import os

file_af = '.MOV'
file_path = 'Zhujingxi'

# Calculate the shake_256 hash value of the file
with open(file_path + file_af, 'rb') as f:
    hash_obj = hashlib.shake_256()
    hash_obj.update(f.read())
hash_value_1 = hash_obj.digest(256)

# Convert the hash value to a binary string
sizebinary = f"{os.path.getsize(file_path + file_af):b}"
binary_hash_value_1 = sizebinary + ''.join(f"{byte:08b}" for byte in hash_value_1)

print(sizebinary)
print(binary_hash_value_1)


def cut_len(lst, lens):
    """
    Split a list into sublists of specified length
    :param lst: The list to split
    :param lens: The length of the sublists
    :return: The list of sublists
    """
    return [lst[i:i + lens] for i in range(0, len(lst), lens)]


def bin_int(lst):
    """
    Convert a list of binary strings to a list of integers
    :param lst: The list of binary strings
    :return: The list of integers
    """
    return [int(''.join(i), 2) for i in lst]


def pattern_cull_method_1(lst):
    """
    Split a list into two sublists, the first containing elements at odd positions and the second containing elements at even positions
    :param lst: The list to split
    :return: The two sublists
    """
    x_cor = lst[::2]
    y_cor = lst[1::2]
    if len(x_cor) > len(y_cor):
        y_cor.append(x_cor[-1])
    return [x_cor, y_cor]


def output_cor(lst):
    """
    Output two sublists to two separate files
    :param lst: The list containing two sublists
    """
    with open('xCor.txt', 'w') as x_cor_file:
        x_cor_file.writelines(f"{c}\n" for c in lst[0])
    with open('yCor.txt', 'w') as y_cor_file:
        y_cor_file.writelines(f"{c}\n" for c in lst[1])


def output_cor_one(lst, lit):
    """
    Merge two sublists into a string and output it to a file
    :param lst: The list containing two sublists
    :param lit: The multiplier
    """
    with open(file_path + '.txt', 'w') as cor_file:
        for counter, x in enumerate(lst[0]):
            cor_file.write(f"{x},{counter * lit},{lst[1][counter]}\n")


def output():
    """
    Main function that calls other functions to process and output the result
    """
    # Split the binary string into substrings of length 8 and convert them to a list of integers
    int_list = bin_int(cut_len(binary_hash_value_1, 8))
    # Split the list of integers into two sublists
    split_list = pattern_cull_method_1(int_list)
    # Output the two sublists to files
    output_cor(split_list)
    # Merge the two sublists into a string and output it to a file
    output_cor_one(split_list, 4)



output()

