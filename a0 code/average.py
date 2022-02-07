
"""
Run python autograder.py 
"""


def average(priceList):
    "Return the average price of a set of fruit"
    "*** YOUR CODE HERE ***"
    sum=0.0
    checkList=[]
    for i in range (0,len(priceList)):
        if priceList[i]not in checkList:
            sum+=priceList[i]
            checkList.append(priceList[i])
    return sum/len(checkList)

print(average([1,1,3,3,4,5]))