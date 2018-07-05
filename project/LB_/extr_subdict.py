

# return 一个新字典 要求 new_dict的建为列表中的元素 缺一个返回Flase
list1 = ['a','c']
dict1={'a':'liusi','lpp':'lsjdl','c':'lsdkjall'}
list2 = []
def extr_sub_dict(list1,dict1):

    techDict = {key: value for key, value in dict1.items() if key in list1 }

    for key in techDict:
        list2.append(key)
    if list1 == list2:
        # return techDict

        print(techDict)
    else:
        # return False
        print(False)


extr_sub_dict(list1,dict1)