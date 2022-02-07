"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def checkPrice(fruitName,fruitPrices):
    return fruitPrices[fruitName]

def buyLotsOfFruit(orderList,fruitPrices):
    totalCost = 0.0             
    for i in range(0,len(orderList)):
        totalCost+=checkPrice(orderList[i][0],fruitPrices)*orderList[i][1]    
    return totalCost
    
def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    "*** YOUR CODE HERE ***"
    price=[]
    for shop in fruitShops:
        price.append(buyLotsOfFruit(orderList,shop.fruitPrices))
    return fruitShops[price.index(min(price))]

    
def shopArbitrage(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        maximum profit in amount
    """
    "*** YOUR CODE HERE ***"
    profit=0.0
    for fruit in orderList:
        allPrice=[]
        for shop in fruitShops:
            allPrice.append(shop.fruitPrices[fruit[0]])
        profit+=(max(allPrice)-min(allPrice))*fruit[1]

    print(profit)


    return profit

def shopMinimum(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        Minimun cost of buying the fruits in orderList
    """
    "*** YOUR CODE HERE ***"
    cost = 0.0
    for fruit in orderList:
        allPrice = []
        for shop in fruitShops:
            allPrice.append(shop.fruitPrices[fruit[0]])
        cost += ( min(allPrice)) * fruit[1]

    return cost

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())

  print(shopArbitrage(orders,shops))
