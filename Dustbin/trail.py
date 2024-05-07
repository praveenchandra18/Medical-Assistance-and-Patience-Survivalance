import pandas as pd

dataframe=pd.read_csv('results.csv')

data_list=dataframe.values.tolist()

cluster_0=[]
cluster_1=[]
cluster_2=[]
cluster_3=[]
cluster_4=[]

for i in range(len(data_list)):
    if(data_list[i][1]==0):
        cluster_0.append(data_list[i])
    elif(data_list[i][1]==1):
        cluster_1.append(data_list[i])
    elif(data_list[i][1]==2):
        cluster_2.append(data_list[i])
    elif(data_list[i][1]==3):
        cluster_3.append(data_list[i])
    elif(data_list[i][1]==4):
        cluster_4.append(data_list[i])

print(cluster_0)
print("---------------")
print(cluster_1)
print("---------------")
print(cluster_2)
print("---------------")
print(cluster_3)
print("---------------")
print(cluster_4)
# # print(cluster_4) 2,3,4 for breakfast lunch and dinner

# print("cluster1 lunch")
# for i in cluster_1:
#     if(i[4]==1):
#         print(i[0])


