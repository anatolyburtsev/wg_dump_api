import filecmp
import os

"""
concatinate two files these types:
file1:
a
b
c

file2:
b
c
d

result:
a
b
c
d
"""


def glue_files(filename_1, filename_2, output_file):
    assert type(filename_1) == type(filename_2) == type(output_file) == str

    f1 = open(filename_1, 'r')
    f2 = open(filename_2, 'r')
    f_out = open(output_file, 'a')
    f2_first_line = f2.readline()
    f1_line = True
    f2_line = True

    while f1_line:
        f1_line = f1.readline()
        if f1_line != f2_first_line:
            f_out.write(f1_line)
        else:
            f_out.write(f2_first_line)
            break

    while f2_line:
        f2_line = f2.readline()
        f_out.write(f2_line)

    f1.close()
    f2.close()
    f_out.close()


if __name__ == "__main__":
    # f1 = "test/file1"
    # f2 = "test/file2"
    # f_out = "test/file_output"
    # f_result = "test/file_12"
    # glue_files(f1, f2, f_out)
    # assert filecmp.cmp(f_out, f_result)
    glue_files("full_dump", "nicknames_dump_8823000_100000000", "full_dump1")
    os.rename("full_dump1", "full_dump")

