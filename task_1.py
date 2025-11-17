def nearly(array):
    sorted_array=sorted(array)
    result={}
    
    for i in range(len(sorted_array)):
        current=sorted_array[i]
        left_diff = float('inf')
        right_diff = float('inf')

        if i<len(sorted_array)-1:
            right_diff=sorted_array[i+1]-current

        if i>0:
            left_diff=current-sorted_array[i-1]
        

        if left_diff<=right_diff:
            result[current]=sorted_array[i-1]

        else: 
            result[current]=sorted_array[i+1]
    return result


#line_size=int(input())
mas=[7,6,5,4,3,2,1]
res=nearly(mas)
result=[]
print(mas)
print(sorted(mas))
for num in mas:
    result.append(res[num])
print(result)
