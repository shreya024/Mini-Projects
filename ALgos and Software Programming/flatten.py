#[1,2,[3,4],[[5,6,[7]]]] to [1,2,3,4,5,6,7]

import numpy as np

arr=[1,2,[3,4],[[5,6,[7]]]]
ans=[]

def flatten(x):
    for item in x:
        if isinstance(item, int):
            ans.append(item)
        else:
            flatten(item)


flatten(arr)
   
print (ans)