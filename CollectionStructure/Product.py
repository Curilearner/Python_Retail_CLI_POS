from collections import namedtuple
from typing import List

Item = namedtuple('Item' ,['sn', 'name', 'price', 'quantity', 'quantitytype'] )
Inventory: List[Item] = []