string1 = u"Ïîëèâàíîâó"
string2 = u"Поливанову"

for c in u"Ïîëèâàíîâó":
    print(repr(c), ord(c))

for c in u"Поливанову":
    print(repr(c), ord(c))

for i in range(0, len(string1)):
    print(ord(string1[i]) - ord(string2[i]))