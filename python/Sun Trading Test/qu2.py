def short_udr(matrix):
    shortest = [matrix[row][0] for row in range(len(matrix))]
    print shortest

    for j in range(1, len(matrix)):
        column = [matrix[row][j] for row in range(len(matrix))]
        print 'col',column
        
        shortest = [ column[row] + 
            min([shortest[k] + sum(column[k:row:(1 if k <= row else -1)])
                for k in range(len(matrix))])
                                                    for row in range(len(matrix))]
            
        print shortest

    return min(shortest)
    
def matr(txt):
    f = open ( txt , 'r')
    l = [ map(int,line.split(',')) for line in f ]
    f.close
    return l 
    
if __name__ == '__main__': 
### PATH TO matrix.txt MAY BE DIFFERENT FOR YOU 
    print 'RES 2:', short_udr(matr('./matrix'))