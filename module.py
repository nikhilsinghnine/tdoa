import numpy
import math


def generateCombinations(array_X, array_Y, array_Z, r):
        array1_X, array1_Y, array1_Z=[], [], []
        if r==len(array_X):
            if array_X not in subArrays_X:
                subArrays_X.append(array_X)
                return
            if array_Y not in subArrays_Y:
                subArrays_Y.append(array_Y)
                return
            if array_Z not in subArrays_Z:
                subArrays_Z.append(array_Z)
                return

        for item_X, item_Y, item_Z in zip(array_X, array_Y, array_Z):
            array1_X=array_X[:]
            array1_X.remove(item_X)
            array2_X=generateCombinations(array1_X, array1_Y, array1_Z, r)

            array1_Y=array_Y[:]
            array1_Y.remove(item_Y)
            array2_Y=generateCombinations(array1_X, array1_Y, array1_Z, r)

            array1_Z=array_Z[:]
            array1_Z.remove(item_Z)
            array2_Z=generateCombinations(array1_X, array1_Y, array1_Z, r)

            element[0]+=1
            if array2_X not in subArrays_X and array2_X:
                    subArrays_X.append(array2_X)
            if array2_Y not in subArrays_Y and array2_Y:
                    subArrays_Y.append(array2_Y)
            if array2_Z not in subArrays_Z and array2_Z:
                    subArrays_Z.append(array2_Z)

def findLocation(x,y,z):
    for j in range(len(x)):
        Ri[j] = math.sqrt((x[j]-xi)**2+(y[j]-yi)**2+(z[j]-zi)**2)
        Rj[j] = math.sqrt((x[j]-xj)**2+(y[j]-yj)**2+(z[j]-zj)**2)
        Rk[j] = math.sqrt((x[j]-xk)**2+(y[j]-yk)**2+(z[j]-zk)**2)
        Rl[j] = math.sqrt((x[j]-xl)**2+(y[j]-yl)**2+(z[j]-zl)**2)

        Rij[j] = Ri[j]-Rj[j]
        Rik[j] = Ri[j]-Rk[j]
        Rkj[j] = Rk[j]-Rj[j]
        Rkl[j] = Rk[j]-Rl[j]

        xji, yji, zji = xj-xi,yj-yi,zj-zi
        xki, yki, zki = xk-xi,yk-yi,zk-zi
        xjk, yjk, zjk = xj-xk,yj-yk,zj-zk
        xlk, ylk, zlk = xl-xk,yl-yk,zl-zk

        A[j] = (Rik[j]*xji-Rij[j]*xki)/(Rij[j]*yki-Rik[j]*yji)
        B[j] = (Rik[j]*zji-Rij[j]*zki)/(Rij[j]*yki-Rik[j]*yji)
        C[j] = (Rik[j]*(Rij[j]**2+xi**2-xj**2+yi**2-yj**2+zi**2-zj**2)- Rij[j]*(Rik[j]**2+xi**2-xk**2+yi**2-yk**2+zi**2-zk**2))/(2*(Rij[j]*yki-Rik[j]*yji))
        D[j] = (Rkl[j]*xjk-Rkj[j]*xlk)/(Rkj[j]*ylk-Rkl[j]*yjk)
        E[j] = (Rkl[j]*zjk-Rkj[j]*zlk)/(Rkj[j]*ylk-Rkl[j]*yjk)
        F[j] = (Rkl[j]*(Rkj[j]**2+xk**2-xj**2+yk**2-yj**2+zk**2-zj**2)- Rkj[j]*(Rkl[j]**2+xk**2-xl**2+yk**2-yl**2+zk**2-zl**2))/(2*(Rkj[j]*ylk-Rkl[j]*yjk))

        G[j] = (E[j]-B[j])/(A[j]-D[j])
        H[j] = (F[j]-C[j])/(A[j]-D[j])
        I[j] = A[j]*G[j]+B[j] 
        J[j] = A[j]*H[j]+C[j]
        K[j] = Rik[j]**2+xi**2-xk**2+yi**2-yk**2+zi**2-zk**2+2*xki*H[j]+2*yki*J[j]
        L[j] = 2*(xki*G[j]+yki*I[j]+2*zki)
        M[j] = 4*(Rik[j]**2)*(G[j]**2+I[j]**2+1)-L[j]**2
        N[j] = 8*(Rik[j]**2)*(G[j]*(xi-H[j])+I[j]*(yi-J[j])+zi)+2*L[j]*K[j]
        O[j] = 4*(Rik[j]**2)*((xi-H[j])**2+(yi-J[j])**2+zi**2)- K[j]**2
        
        sz[j] = (N[j]/(2*M[j]))+math.sqrt(((N[j]/(2*M[j]))**2-(O[j]/M[j])))
        sy[j] = I[j]*sz[j]+J[j]
        sx[j] = G[j]*sz[j]+H[j]

    return sx, sy, sz

if __name__ == '__main__':

    x=[13970.04, 43271.75, 71300.97, 95219.61]      
    y=[-18557.80, -57444.36, -94639.05, -126379.45]
    z=[22270.68, 34057.40, 24218.86, 18483.85]

    array_X=[0.0, -25000.00, 23000.00, -101000.00, -2611.204, 1859.424, -169.088]#, 4642.943, 1826.389, 728.806, 4633.135
    array_Y=[0.0, -2315.226, 35000.213, -167000.00, 547.975, 4537.568, 2315.324]#, 5033.602, -64205.797, -57207.506, 5044.402
    array_Z=[0.0, 500.00, 45.00, -3000.00, 0.982, 6.256, 6.155]#, -0.916, -322.926, -254.013, 0.450


    #xi,yi,zi = 0.0, 0.0, 0.0  #bpur
    #xj,yj,zj = -25000.00, -2315.226, 500.00 #Nilgiri
    #xk,yk,zk = 23000.00, 35000.213, 45.00 #Amarda
    #xl,yl,zl = -101000.00, -167000.00, -3000.00 #P1

    #xi, xj, xk, xl= 0.0, -25000.00, 23000.00, -101000.00
    #yi, yj, yk, yl= 0.0, -2315.226, 35000.213, -167000.00
    #zi, zj, zk, zl= 0.0, 500.00, 45.00, -3000.00

    Ri, Rj, Rk, Rl, Rij, Rik, Rkj, Rkl= {},{},{},{},{},{},{},{}
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O={},{},{},{},{},{},{},{}, {},{},{},{},{},{},{}
    sz, sy, sx={},{},{}


    subArrays_X=[]
    subArrays_Y=[]
    subArrays_Z=[]
    element=[0]
    generateCombinations(array_X, array_Y, array_Z, 4)
    print 'Total number of combinations: '+str(len(subArrays_X))+'\n'
    print 'Combinations: '
    for i in range(len(subArrays_X)):
        print 'X: '+str(subArrays_X[i])+'   Y:'+str(subArrays_X[i])+'   Z:'+str(subArrays_Z[i])
    X_receiver=[]
    Y_receiver=[]
    Z_receiver=[]
    indices_X=subArrays_X[-1]
    indices_Y=subArrays_Y[-1]
    indices_Z=subArrays_Z[-1]
    for i,j,k in zip(indices_X, indices_Y, indices_Z):
        X_receiver.append(i)
        Y_receiver.append(j)
        Z_receiver.append(k)
    print 'X coordinate: '+str(X_receiver)
    print 'Y coordinate: '+str(Y_receiver)
    print 'Z coordinate: '+str(Z_receiver)
    print '\n'

    xi, xj, xk, xl= [X_receiver[i] for i in range(4)]
    yi, yj, yk, yl= [Y_receiver[i] for i in range(4)]
    zi, zj, zk, zl= [Z_receiver[i] for i in range(4)]



    locations= findLocation(x,y,z)
    true_positions = numpy.column_stack((x, y, z))
    true_positions=true_positions.T
    array=[]
    for location in locations:
        for value in location.values():
            temp=value
            array.append(temp)
    locations= numpy.array(array).reshape(3, len(location))
    for i in range(4):
        print (true_positions[:,i]-locations[:,i])#/true_positions[:,i]