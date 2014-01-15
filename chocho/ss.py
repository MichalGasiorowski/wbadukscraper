import os
import errno

folder_names = ["Part 1 - Life and Death on the Second Line",
"Part 2 - Part Two Six-Space Eye Shapes in the Corner",
"Part 3 - Eight Space Eye Groups in the Corner",
"Part 4 - The Comb Patterns",
"Part 5 - The Carpenter's Square",
"Part 6 - Second Line Shapes on the Side",
"Part 7 - Third Line Shapes on the Side",
"Part 8 - Fourth Line Shapes on the Side",
"Part 9 - Applications The Star-Point and the 3-3 Point",
"Part 10 - Applications Various Ways of Invading"]

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

problem_counts = [22, 25, 31, 34, 28, 26, 25, 16, 10, 12]

for i in range(1, 10):
    folder_to_create = folder_names[i]
    make_sure_path_exists(folder_to_create)
    for num in range(1, problem_counts[i]+1):
        sgf_name = str(i + 1) + "-" + str(num) + ".sgf"
        sgf_inside = "(;CA[Windows-1252]AP[MultiGo:4.4.4]C[Part " + str(i + 1) + " - Pattern " + str(num) + "]MULTIGOGM[1])"
        with open(folder_to_create + "/" + sgf_name,'wt') as ff:
            ff.write(sgf_inside)
