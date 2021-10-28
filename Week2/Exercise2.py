###################################################
###################################################
########### Aviel Berkowitz (211981105) ###########
###################################################
###################################################

# Class Exercise:
#
# def convert2arff(num_of_files):
#    fout = open("hospital.arff", "w")
#    fout.write("@relation patients_temperatures\n")
#    fout.write("@attribute ward numeric\n")
#    fout.write("@attribute patients_ID numeric\n")
#    fout.write("@attribute time numeric\n")
#    fout.write("@attribute temperature numeric\n\n")
#    fout.write("@data\n")
#    for ward in range(1, num_of_files+1):
#        fin = open(str(ward)+".txt", "r")
#        for time in range(60*24):
#            s = fin.readline().split()
#            for patient in range(len(s)):
#                fout.write(str(ward)+"," + str(patient+1)+"," + str(time)+","+s[patient]+"\n")
#        fin.close()
#    fout.close()

import math


def F_to_C(deg):
    return (deg - 32) * 5 / 9


def is_valid_temp(deg):
    deg = F_to_C(deg) if deg > 43 else deg
    return 36 <= deg <= 43, deg


def temp_to_category(deg):
    if is_valid_temp(deg)[0]:
        return "Low" if deg >= 37 else "High"
    else:
        return "?"


def convert2arff(num_of_files):
    for ward in range(1, num_of_files + 1):
        fout = open("temp" + str(ward) + ".txt", "w")
        fout.write("@relation patients_temperatures\n")
        fout.write("@attribute patients_ID numeric\n")
        fout.write("@attribute time numeric\n")
        fout.write("@attribute temperature numeric\n\n")
        fout.write("@data\n")
        fin = open(str(ward) + ".txt", "r")
        for time in range(60 * 12):  # from 00:00 to 11:59 = 60 mins * 12 hours
            s = fin.readline().split()
            for patient in range(len(s)):
                fout.write(str(patient + 1) + ", " + str(time) + ", " + temp_to_category(float(s[patient])) + "\n")
        fin.close()
    fout.close()


def stdv(ward_num):
    fin = open(str(ward_num) + ".txt", "r")
    sum = 0
    sum_squared = 0
    size = 0
    for time in range(60 * 24):  # from 00:00 to 23:59 = 60 mins * 24 hours
        s = fin.readline().split()
        for patient in range(len(s)):
            valid, x = is_valid_temp(float(s[patient]))
            if valid:
                size += 1
                sum += x
                sum_squared += x ** 2
    fin.close()
    mean = sum / size
    variance = sum_squared / size - mean ** 2 if (sum_squared / size - mean ** 2) >= 0 else 0
    return math.sqrt(variance)


if __name__ == '__main__':
    convert2arff(3)
    print("Ward 1 standard deviation: " + str(stdv(1)))
    print("Ward 2 standard deviation: " + str(stdv(2)))
    print("Ward 3 standard deviation: " + str(stdv(3)))

