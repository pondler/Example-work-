"""Homework 2, part 1, Christopher McLeod, 00947553
"""
import scipy
from scipy import misc
import matplotlib.pyplot as plt
import numpy as np

def crop(F, T = 0.0, B = 0.0, L = 0.0, R = 0.0):
   """Crop image represented by matrix F. T,B,L,R indicate 
how much of the image should be removed from the top, bottom,
left, and right of the original image.
"""
#  Create assertions for parameter values 
   assert (0<=T<1), 'Error: T must be in [0,1)'
   assert (0<=B<1), 'Error: B must be in [0,1)'
   assert (0<=L<1), 'Error: L must be in [0,1)'
   assert (0<=R<1), 'Error: R must be in [0,1)' 
   assert (T+B<1), 'Error: Ensure T + B < 1'
   assert (L+R<1), 'Error: Ensure L+R<1'

#  Define crop boundaries
   m, n, k = F.shape
   Rt = int(np.floor(T*m))
   Rb = int(np.floor(B*m))
   Rl = int(np.floor(L*n))
   Rr = int(np.floor(R*n))
   F = F[ Rt : m-Rb , Rl : n-Rr, :]

#  Normalise F
   big = F.max()
   F = (1/big)*F

   return F

def smooth(F):
    """ Apply a simple smoothing procedure to image matrix F. The code breaks the 3D matrix into 3 2D
    matrices, and to each, segments the matrix into cells surrounded by 8,5 or 3 other cells and takes
    the average of itself and the surrounding cells.
    """

    m, n, k = F.shape
    for i in range(k):

#   average for cells surrounded by 8 others
#   define Central cells,C, the ones with 8 adjacent values
#   average by cyling though +/-1 combinations in (x,y) directions from initial cell
        C = F[1:m-1,1:n-1,i]
        for ind, value in np.ndenumerate(C):
            C[ind[0],ind[1]]=(1/9)*(int(value)+int(F[ind[0]+1,ind[1],i])+
              int(F[ind[0]-1,ind[1],i])+int(F[ind[0],ind[1]+1,i])+
              int(F[ind[0],ind[1]-1,i])+int(F[ind[0]+1,ind[1]+1,i])+
              int(F[ind[0]-1,ind[1]+1,i])+int(F[ind[0]-1,ind[1]-1,i])+int(F[ind[0]+1,ind[1]-1,i]))

#   average for corners clockwise from (0,0)
        X = 0.25*(int(F[0,0,i]) + int(F[0,1,i]) + int(F[1,0,i]) + int(F[1,1,i]) )
        Y = 0.25*(int(F[m-1,0,i]) + int(F[m-1,1,i]) + int(F[m-2,0,i]) + int(F[m-2,1,i]) )
        Z = 0.25*(int(F[m-1,n-1,i]) + int(F[m-2,n-1,i]) + int(F[m-1,n-2,i]) + int(F[m-2,n-2,i]) )
        T = 0.25*(int(F[0,n-1,i]) + int(F[1,n-1,i]) + int(F[0,n-2,i]) + int(F[1,n-2,i]) )
        
#   Create North(N), East(E), South(S), West(W) edges ecluding corners    	
#   average for edges excluding corners clockwise from (0,0)
        N = F[0,1:n-1,i]
        for ind, value in np.ndenumerate(N):
            N[ind[0]] = (1/6)*(int(value)+int(F[0+1,ind[0],i])+int(F[0,ind[0]+1,i])+
              int(F[0,ind[0]-1,i])+int(F[0+1,ind[0]+1,i])+int(F[0+1,ind[0]-1,i]))
        E = F[1:m-1,0,i]
        for ind, value in np.ndenumerate(E):
            E[ind[0]] = (1/6)*(int(value)+int(F[ind[0]+1,0,i])+int(F[ind[0]-1,0,i])+
              int(F[ind[0],0+1,i])+int(F[ind[0]+1,0+1,i])+int(F[ind[0]-1,0+1,i]))
        S = F[m-1,1:n-1,i]
        for ind, value in np.ndenumerate(S):
            S[ind[0]] = (1/6)*(int(value)+int(F[m-1-1,ind[0],i])+int(F[m-1,ind[0]+1,i])+
              int(F[m-1,ind[0]-1,i])+int(F[m-1-1,ind[0]+1,i])+int(F[m-1-1,ind[0]-1,i]))
        W = F[1:m-1,n-1,i]
        for ind, value in np.ndenumerate(W):
            W[ind[0]] = (1/6)*(int(value)+int(F[ind[0]+1,n-1,i])+int(F[ind[0]-1,n-1,i])+
              int(F[ind[0],n-1-1,i])+int(F[ind[0]+1,n-1-1,i])+int(F[ind[0]-1,n-1-1,i]))
    	
# 	Reassign F with its averaged segements
        F[1:m-1,1:n-1,i] = C
        F[0,1:n-1,i] = N
        F[1:m-1,0,i] = E
        F[m-1,1:n-1,i] = S
        F[1:m-1,n-1,i] = W
        F[0,0,i] = X
        F[m-1,0,i] = Y
        F[m-1,n-1,i] = Z
        F[0,n-1,i] = T
    
#   Normalise F
    big = F.max()
    F = (1/big)*F
    
    return F
        

def compress(F2d,C):
    """ Compresses 2D image. P determined by solving C*mn = m*P + P*1 + P*n to match the compressed size of the array to the sum of the three elements creaed.
    """
#   Get dimensions of F2d
    m,n = F2d.shape
    
#   Make sure parameter is in the boundary
    assert (0<C<1), "Ensure compression parameter C is in (0,1)"
    
#   Initialise the first SVD composition
    U, s, V = np.linalg.svd(F2d, full_matrices=False)
    
#   Determine P
    P = int(np.floor(C*m*n/(m+n+1)))
    
    U = U[:,:P]
    s =s[:P] 
    V = V[:P,:]
    
    return U, s, V 

def reconstruct(U,s,V, flag_type=False): #rename/add/remove input variables as needed
    """ Reconstruct an approximate 2-d image matrix from the "compressed" variables
    generated by compress
    """
#   Generate S, filling the diagonals with values of s
    S = np.diag(s)

#   Reconstruct compressed image
    Fcomp = U.dot(S).dot(V)

#   display the image if the flag_type is true
    if (flag_type == True):
        plt.figure()
        plt.imshow(Fcomp)
        
    return Fcomp
    
    

if __name__ == '__main__':
    #Read and display image
    F = scipy.misc.imread("image.jpg")
    plt.figure()
    plt.imshow(F)


# The code below can be used to test if
# the code is functioning in a "reasonable" manner.

#    T,B,L,R = 0.1,0.2,0.3,0.4

#    G = crop(F,T,B,L,R)
#    plt.figure()
#    plt.imshow(G)
#    plt.show()
    
#    G = smooth(F)
#    plt.figure()
#    plt.imshow(G)
    
#    a1,a2,a3 = compress(F.mean(2),0.1)
#    G = reconstruct(a1,a2,a3)
#    plt.figure()
#    plt.imshow(G,'gray')