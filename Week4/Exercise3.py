######################################################
######################################################
###########  Aviel Berkowitz   (211981105)  ##########
###########  Itamar Cohen      (318558236)  ##########
######################################################
######################################################

import random

N = 5  # no. of attributes
MINSUP = 0.125


# Creates a file named filename containing m sorted itemsets of items 0..N-1
def createfile(m, filename):
    f = open(filename, "w")
    for line in range(m):
        itemset = []
        for i in range(random.randrange(N) + 1):
            item = random.randrange(N)  # random integer 0..N-1
            if item not in itemset:
                itemset += [item]
        itemset.sort()
        for i in range(len(itemset)):
            f.write(str(itemset[i]) + " ")
        f.write("\n")
    f.close()


# Returns true iff all of smallitemset items are in bigitemset (the itemsets are sorted lists)
def is_in(smallitemset, bigitemset):
    s = b = 0  # s = index of smallitemset, b = index of bigitemset
    while s < len(smallitemset) and b < len(bigitemset):
        if smallitemset[s] > bigitemset[b]:
            b += 1
        elif smallitemset[s] < bigitemset[b]:
            return False
        else:
            s += 1
            b += 1
    return s == len(smallitemset)


# Returns a list of itemsets (from the list itemsets) that are frequent
# in the itemsets in filename
def frequent_itemsets(filename, itemsets):
    f = open(filename, "r")
    filelength = 0  # filelength is the no. of itemsets in the file. we
    # use it to calculate the support of an itemset
    count = [0] * len(itemsets)  # creates a list of counters
    line = f.readline()
    while line != "":
        filelength += 1
        line = line.split()  # splits line to separate strings
        for i in range(len(line)):
            line[i] = int(line[i])  # converts line to integers
        for i in range(len(itemsets)):
            if is_in(itemsets[i], line):
                count[i] += 1
        line = f.readline()
    f.close()
    freqitemsets = []
    for i in range(len(itemsets)):
        if count[i] >= MINSUP * filelength:
            freqitemsets += [itemsets[i] + [count[i]/filelength]]
    return freqitemsets


def create_kplus1_itemsets(kitemsets, filename):
    kplus1_itemsets = []
    kitemsets_no_support = [x[:-1] for x in kitemsets]
    for i in range(len(kitemsets) - 1):
        j = i + 1  # j is an index
        # compares all pairs, without the last item, (note that the lists are sorted)
        # and if they are equal than adds the last item of kitemsets[j] to kitemsets[i]
        # in order to create k+1 itemset
        while j < len(kitemsets_no_support) and kitemsets_no_support[i][:-1] == kitemsets_no_support[j][:-1]:
            kplus1_itemset = kitemsets_no_support[i] + [kitemsets_no_support[j][-1]]
            for k in range(len(kplus1_itemset)):
                flag = kplus1_itemset[:k] + kplus1_itemset[k + 1:] in kitemsets_no_support
                if not flag:
                    break

            if flag:
                kplus1_itemsets += [kplus1_itemset]
            j += 1
    # checks which of the k+1 itemsets are frequent
    return frequent_itemsets(filename, kplus1_itemsets)


def create_1itemsets(filename):
    it = []
    for i in range(N):
        it += [[i]]
    return frequent_itemsets(filename, it)


def minsup_itemsets(filename):
    minsupsets = kitemsets = create_1itemsets(filename)
    while kitemsets != []:
        kitemsets = create_kplus1_itemsets(kitemsets, filename)
        minsupsets += kitemsets
    return minsupsets


# createfile(100, "itemsets.txt")
print(minsup_itemsets("itemsets.txt"))
