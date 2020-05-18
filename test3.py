import numpy as np
import shapefile
import matplotlib.pyplot as plt
from decimal import Decimal

an_array = np.array([[Decimal('8'), Decimal('2'), Decimal('-2')],
                     [Decimal('-4'), Decimal('1'), Decimal('7')],
                     [Decimal('6'), Decimal('3'), Decimal('9')]], dtype=Decimal)
sorted_array = an_array[np.argsort(an_array[:, 1])]
print(sorted_array)
