# exo1
a = 10
b = 5
c = 29
x = '3'
d = {}
li = [2, 4, 10]
# 1
a % b == 0 and a <= c
# 2:
not(('a' < x < 'z') or ('A' < x < 'Z'))
# 3
x in d.keys()
# 4
len(li) != 0 and (li[-1] == a or li[-1] == b or li[-1] == c)
print(li)
# exo2
li = []
mot = input("Tape des mots")
rejouer = "oui"
while mot != 'stop' and rejouer == "oui":
    mot = input("Tape des mots")


def verifierMot(mot):
    for chr in mot:
        if chr < 'a' or chr > 'z':
            return False
    return True
