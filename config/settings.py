"""
when clear long postion
Sell price = cur price * sell_offset

when clear short position
Sell price = cur price * Buy_Offset
"""
SELL_OFFSET = 0.999 
BUY_OFFSET = 1.001