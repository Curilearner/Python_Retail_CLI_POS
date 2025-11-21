from collections import namedtuple

Item = namedtuple('Item' ,['sn', 'name', 'price', 'quantity', 'quantitytype'] )
Inventory: List[Item] = []