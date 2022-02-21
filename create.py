import json
import re

def findkeysvalues(inputDict, key):
    if isinstance(inputDict, list):
        for i in inputDict:
            for x in findkeysvalues(i, key):
               yield x
    if isinstance(inputDict, dict):
        if key in inputDict:
            yield inputDict[key]
        for j in inputDict.values():
            for x in findkeysvalues(j, key):                
                yield x

def process_JSON_value(jsonFileInput, parentInputKey, key):
    with open(jsonFileInput) as jsonFile:      
        data = json.load(jsonFile)
        Dict = { }
        for i in data:
            if i == parentInputKey:
                Dict[i] = data[i]
        return list(findkeysvalues(Dict, key))

def createRulesJSON():
    
    with open("test1.json") as jsonFile:
        data = json.load(jsonFile)

    Dict = { }
    
    rules_items_source = list(findkeysvalues(data, "source"))
    # print (rules_items_source)
    for p in data:
        print("ooooooooooo",p)
        Dict[p] = { }
        count = 0
        for i in rules_items_source:
            print ("ssssssssssssssssss",rules_items_source)
            print("kkkkkkkkkkkkkk",i)
            x = re.findall("\w+", i[0])
            print("bbbbbbbbbbbbbbbbbbb",x)
            sourceItems = process_JSON_value("test.json", x[0], "compname")
            if count == 0:
                print("mmmmmmmmmmmmmmmmm",sourceItems)
                Dict[p]['source'] = sourceItems
                count = count +1

    
    rules_items_dest = list(findkeysvalues(data, "dest"))
    for p in data:
        # Dict[p] = { }
        count = 0
        for i in rules_items_dest:
            x = re.findall("Microservice.\w+", i[0])
            y = x[0].split(".")
            items = process_JSON_value("test.json", y[0], y[1])
            if count == 0:
                Dict[p]['dest'] = items
                count = count +1

    
    rules_items_port = findkeysvalues(data, "port")
    for i in rules_items_port:
        for p in data:
            if count == 0:
                Dict[p]['port'] = i
                count = count + 1
    print(Dict)

    with open("sample.json", "w") as file:
        json.dump(Dict, file)

createRulesJSON()
