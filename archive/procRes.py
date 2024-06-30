import numpy as np
import pandas as pd


def procRes(outArr,titles):
#     print(outArr)

    outArrT = np.array(np.transpose(np.transpose(outArr))) #transpose output twice
    # print(outArrT)
#     print(np.array(outArrT[:,1]).astype(float))
    if len(outArrT)>1:
        indices = np.argsort(np.array(outArrT[:,5]).astype(float)) #indices to sort by descending profitability percentage
        indices = indices[::1] #flipping indices
        outArrT = outArrT[indices] #reorganizing output array based on sorted indices
    df2 = pd.DataFrame(outArrT,columns = titles) #outputting data as dataframe
    
    return df2