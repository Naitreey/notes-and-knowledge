# algorithms
## sorting problem
- selection sort
- insertion sort (loop version, recursion version)
- bubble sort
- merge sort (sentinel value version, non-sentinel value version)

## searching problem
- linear search
- binary search

# exercises
2.1-3
pseudocode:
```
result=NIL
for i=1 to A.length
    if A[i]==v
        result=i
        break
```

2.1-4
Input: Two array of n-bit binary integers, A, B
Output: An array of (n+1)-bit binary integer C, such that C=A+B

pseudocode:
```
pos=0
for i=1 to A.length
    result=A[i]+B[i]+pos
    C[i]=result%2
    if(result>1)
        pos=1
    else
        pos=0
C[A.length+1]=pos
```

2.2-1
\Theta(n^2)

2.2-2
pseudocode:
```
for i=1 to A.length-1
    min=A[i]
    for j=i+1 to A.length
        if A[j]<min
            min=A[j]
            pos=j
temp=A[i]
A[i]=A[pos]
A[pos]=temp

```
running time:
\Theta(n^2) for all cases

2.3-2
pseudocode:
Merge(A, start, middle, end)
```
i,j=0
lenL=middle-start+1
lenR=end-middle
create arrL[lenL] and arrR[lenR] new array
initialize two arrays with values of two subarrays
for k=start to end
    if i==lenL
        A[k]=arrR[j]
        j++
    else if j==lenR
        A[k]=arrL[i]
        i++
    else if arrL[i]<=arrR[j]
        A[k]=arrL[i]
        i++
    else
        A[k]=arrR[j]
        j++
```

2.3-4
recursive insertion sort algorithm
pseudocode:
insertion-sort-recursive(A,n)
```
if n>1
    insertion-sort-recursive(A,n-1)
    //insert the n-th element into (n-1) array
    insert(A,n)
```
insert(A,n)
```
key=A[n]
i=n-1
while i>0 and A[i]>key
    A[i+1]=A[i]
    i--
A[i+1]=key
```
recurrence equation:
T(n)=\begin{cases}
1           & \text{if $n=1$},\\
T(n-1)+3n+1 & \text{if $n>1$}
\end{cases}

可以算出 worst-case running time: \Theta(n^2)
