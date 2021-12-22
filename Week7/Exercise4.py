import math

'''
This function converts the data from an .idx binary file of images and labels
to a .txt file, when every line represents a picture and the last number in the
row is the the label. Every pixel is stored as 0 if its value < shade, else 1.
This is in order to have a more convenient way of accessing the data.
'''
def idx2txt(images, labels, shade, output_path):
    fout = open(output_path, "w")
    fimages = open(images, "rb")
    flabels = open(labels, "rb")
    flabels.seek(8)
    fimages.seek(16)
    x = fimages.read(1)
    while x != b"":
        fout.write('0 ' if ord(x) < shade else '1 ')
        for i in range(783):
            fout.write('0 ' if ord(fimages.read(1)) < shade else '1 ')
        fout.write(str(ord(flabels.read(1))) + '\n')
        x = fimages.read(1)
    fout.close()
    fimages.close()
    flabels.close()


def txt2data(filename):
    f = open(filename, "r")
    lines = f.readlines()
    data = []
    for l in lines:
        data.append([int(i) for i in l.split(' ')])

    return data


def split(examples, used, trait):
    """
    examples is a list of lists. every list contains the attributes, the last item is the class. all items are 0/1.
    splits examples into two lists based on trait (attribute).
    updates used that trait was used.
    """
    newEx = [[], []]  # newEx is a list of two lists, list of Ex that Ex[trait]=0 and list of Ex that Ex[trait]=1
    if trait < 0 or trait > len(examples[0]) - 2 or used[trait] == 0:
        return newEx  # illegal trait
    for e in examples:
        newEx[e[trait]] += [e]
    used[trait] = 0  # used is a list that marks trait as used
    return newEx


def isSameClass(examples):
    """
    returns 0 if all the examples are classified as 0.
    returns 1 if all the examples are classified as 1.
    returns 7  if there are no examples.
    returns -2 if there are more zeros than ones.
    returns -1 if there are more or equal ones than zeros.
    """
    if examples == []:
        return 7
    zo = [0, 0]  # zo is a counter of zeros and ones in class
    for e in examples:
        zo[e[-1]] += 1
    if zo[0] == 0:
        return 1
    if zo[1] == 0:
        return 0
    if zo[0] > zo[1]:
        return -2
    else:
        return -1


def infoInTrait(examples, i):
    """
    calculates the information in trait i using Shannon's formula
    """
    count = [[0, 0], [0, 0]]  # [no. of ex. with attr.=0 and clas.=0,no. of ex. with attr.=0 and clas.=1],
    # [no. of ex. with attr.=1 and clas.=0,no. of ex. with attr.=1 and clas.=1]
    for e in examples:
        count[e[i]][e[-1]] += 1
    x = 0
    # Shannon's formula
    if count[0][0] != 0 and count[0][1] != 0:
        x = count[0][0] * math.log((count[0][0] + count[0][1]) / count[0][0]) + \
            count[0][1] * math.log((count[0][0] + count[0][1]) / count[0][1])
    if count[1][0] != 0 and count[1][1] != 0:
        x += count[1][0] * math.log((count[1][0] + count[1][1]) / count[1][0]) + \
             count[1][1] * math.log((count[1][0] + count[1][1]) / count[1][1])
    return x


def minInfoTrait(examples, used):
    """
    used[i]=0 if trait i was already used. 1 otherwise.

    Returns the number of the trait with max. info. gain.
    If all traits were used returns -1.
    """
    minTrait = m = -1
    for i in range(len(used)):
        if used[i] == 1:
            info = infoInTrait(examples, i)
            if info < m or m == -1:
                m = info
                minTrait = i
    return minTrait


def build(examples, max_len):  # builds used
    used = [1] * (len(examples[0]) - 1)  # used[i]=1 means that attribute i hadn't been used
    return recBuild(examples, used, 0, max_len, 0)


def recBuild(examples, used, parentMaj, max_depth, depth):
    """
    Builds the decision tree.
    parentMaj = majority class of the parent of this node. the heuristic is that if there is no decision returns parentMaj
    """
    cl = isSameClass(examples)
    if cl == 0 or cl == 1:  # all zeros or all ones
        return [[], cl, []]
    if cl == 7:  # examples is empty
        return [[], parentMaj, []]
    trait = minInfoTrait(examples, used)
    if trait == -1:  # there are no more attr. for splitting
        return [[], cl + 2, []]  # cl+2 - makes cl 0/1 (-2+2 / -1+2)
    x = split(examples, used, trait)
    if (depth < max_depth):
        left = recBuild(x[0], used[:], cl + 2, max_depth, depth + 1)
        right = recBuild(x[1], used[:], cl + 2, max_depth, depth + 1)
        return [left, trait, right]
    else:
        return [[], cl + 2, []]


def recClassifier(dtree, traits):  # dtree is the tree, traits is an example to be classified
    if dtree[0] == []:  # there is no left child, means arrive to a leaf
        return dtree[1]
    return recClassifier(dtree[traits[dtree[1]] * 2], traits)  # o points to the left child, 2 points to the right child


def classifier(dtree, traits):  # same as the former without recursion
    while dtree[0] != []:
        dtree = dtree[traits[dtree[1]] * 2]
    return dtree[1]


def build_classifier(data_fn, depth):
    # f = open(data_fn, "r")
    # lines = f.readlines()
    original_data = txt2data(data_fn)
    trees = []
    # for l in lines:
    #     original_data.append([int(i) for i in l.split(' ')])

    completed = 0
    for i in range(10):
        alt_data = []
        for line in original_data:
            tmp = line.copy()
            tmp[-1] = 1 if line[-1] == i else 0
            alt_data.append(tmp)

        trees.append(build(alt_data, depth))
        completed += 10
        print('completed: ' + str(completed) + '%')

    return trees
    #print(trees)


def classify(ten_trees_model, image):
    digits = []
    digit = 0
    for model in ten_trees_model:
        if classifier(model, image) == 1:
            digits.append(digit)
        digit += 1
    return digits


def tester(ten_trees_model, test_fn):
    tests = txt2data(test_fn)
    correct = 0
    for test in tests:
        correct_label = test[-1]
        classified_digits = classify(ten_trees_model, test[:-1])
        if len(classified_digits) == 1 and classified_digits[0] == correct_label:
            correct += 1
    return 100 * correct / len(tests)


def threshold(train_fns, test_fns, depth):
    best_shade = 0
    best_percentage = 0
    #for i in range(256):
    for i in range(121, 124, 2):
        # idx2txt("train-images.idx3-ubyte", "train-labels.idx1-ubyte", i)
        idx2txt(train_fns[0], train_fns[1], i, 'data.txt')
        idx2txt(test_fns[0], test_fns[1], i, 'test.txt')
        cur_percentage = tester(build_classifier('data.txt', depth), 'test.txt')
        if cur_percentage > best_percentage:
            best_percentage = cur_percentage
            best_shade = i

        print('completed checking shade ' + str(i) + ', percentage: ' + str(cur_percentage))

    print('best percentage :' + str(best_percentage))
    print('best shade: ' + str(best_shade))
    return best_shade


if __name__ == '__main__':
    #idx2txt("train-images.idx3-ubyte", "train-labels.idx1-ubyte", 130, "data.txt")
    #idx2txt('t10k-images.idx3-ubyte', 't10k-labels.idx1-ubyte', 130, 'test.txt')
    #ten_trees_model = build_classifier('data.txt', 27)
    #print(tester(ten_trees_model, 'test.txt')) #80.71!!!!!!!!!!


    threshold(['train-images.idx3-ubyte', 'train-labels.idx1-ubyte'], ['t10k-images.idx3-ubyte', 't10k-labels.idx1-ubyte'], 27)

    #completed checking shade 130, percentage: 80.71
    #completed checking shade 120, percentage: 81.03
    #completed checking shade 122, percentage: 81.35
    #completed checking shade 124, percentage: 80.96




# e = [[1, 0, 0, 0, 1, 0, 1, 0],
#      [0, 1, 1, 0, 0, 1, 0, 1],
#      [1, 1, 1, 0, 0, 0, 0, 0],
#      [1, 1, 0, 1, 1, 0, 1, 0],
#      [0, 0, 1, 1, 1, 1, 1, 1],
#      [1, 0, 1, 1, 0, 1, 0, 0],
#      [1, 0, 0, 1, 0, 0, 0, 1],
#      [1, 1, 0, 0, 1, 0, 1, 0],
#      [0, 0, 1, 1, 0, 1, 1, 1],
#      [1, 1, 1, 1, 1, 0, 1, 0]]
#
# t = build(e, 4)
# print(classifier(t, [0, 1, 1, 1]))
