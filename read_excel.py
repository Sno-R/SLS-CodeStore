import pandas as pd
import numpy as np

data = pd.read_excel('C:/Users/Admintrator/Desktop/影刀运行文件/抖音店铺配置-飞鸽.xlsx')

list1 = np.array(data).tolist()

for i in list1:
    print(i[5])

print(list1)



# print(data.shape)

# for i in range(1, data.shape[0]):
#     print(i)

