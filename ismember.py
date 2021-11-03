def ismember(a, b):
    '''
    <ismember> is a function equivalent to MATLAB ismember 
    It will return indice of the elements of a list 'b'    
    that are same as the elements of another list 'a'.     
    If the same element(s) with an element in 'a' do not   
    exist in 'b', it will give np.nan values
    
    @@ example 1 @@
    a = [1,5,10]
    b = [1,2,3,4,5,6,7,8,9,10]
    c = ismember(a,b)
    c = [0, 4, 9]
    
    @@ example 2 @@
    x = [1,3,4,9]
    y = [1,0,9]
    z = ismember(x,y)
    z = [0, nan, nan, 2]
    
    This code is from Stack Overflow. See the link:
    https://stackoverflow.com/questions/15864082/python-equivalent-of-matlabs-ismember-function
    Find sfstewman's answer! 
    
    '''
    
    import numpy as np
    bind = {}
    for i, elt in enumerate(b):
        if elt not in bind:
            bind[elt] = i
    return [bind.get(itm, np.nan) for itm in a]  # np.nan can be replaced as any.

