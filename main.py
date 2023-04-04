dict = {"vincent": 9.0, "shelby": 7.0}
sortedDict = sorted(dict.items(), key=lambda x:x[1])
print(sortedDict)
for i in dict:
    print()
    print(dict[i])
    print()