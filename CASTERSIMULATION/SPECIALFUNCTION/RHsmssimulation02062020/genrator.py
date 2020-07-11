

def itteration(my_list):
    for i in my_list:
        for j in i:
            yield j

my_list = [(1,2),(3,4),(5,6)]


a = next(itteration(my_list))
b = next(itteration(my_list))



print(a)
print(b)