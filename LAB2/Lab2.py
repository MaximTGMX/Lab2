import numpy as np
import cv2 as cv
import math

def set_values(a):
    if a==1:
        coord = [
            [100, 400, 200], [100, 100, 300], [100, 100, 100]
        ]
    else:
        coord = [[0, 300, 300, 0],
                 [0, 0, 300, 300],
                 [100, 100, 100, 100]
                 ]
    res = [720, 1280]
    origine = [200, 200]
    blank = np.zeros((res[0], res[1], 3), dtype='uint8')
    return coord,res,origine,blank

def m_inmultire(m1,m2):
    result = [[sum(a * b for a, b in zip(m1_row, m2_col)) for m2_col in zip(*m2)] for m1_row in m1]
    return result

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result

def create_axis(blank,origine,res):
    cv.line(blank, (origine[0], 0), (origine[0], res[0]), (255, 0, 0), 1)
    cv.line(blank, (0, origine[1]), (res[1], origine[1]), (255, 0, 0), 1)

def create_polygon(blank,origine,coord,color):
    for i in range(len(coord)-2):
        for j in range(len(coord[i])-1):
            cv.line(blank, (origine[0]+coord[i][j], origine[1]+coord[i+1][j]), (origine[0]+coord[i][j+1], origine[1]+coord[i+1][j+1]), (color[0], color[1], color[2]), 3)
    cv.line(blank, (origine[0]+coord[0][len(coord[0])-1], origine[1]+coord[1][len(coord[0])-1]), (origine[0]+coord[0][0], origine[1]+coord[1][0]), (color[0], color[1], color[2]), 3)

def set_new_coords(coord,a):
    for i in range(3):
        for j in range(3):
            coord[i][j] = int(a[i][j])
    return coord

def ex1(coord,Q,V):
    m1 = [[math.sqrt(3) / Q[0] * 100, -1 / Q[1] * 100, 3 - math.sqrt(3)],
          [1 / Q[0] * 100, math.sqrt(3) / Q[1] * 100, 1 - math.sqrt(3)],
          [0, 0, 1]]

    m2 = [[1, 0, V[0]],
          [0, 1, V[1]],
          [0, 0, 1]]

    t1 = m_inmultire(m2, m1)
    t2 = m_inmultire(t1, coord)
    coord = set_new_coords(coord,t2)
    return coord

def ex2(coord,Q):
    m1 = [[1, 0, Q[0]/100],
          [0, 1, Q[1]/100],
          [0, 0, 1]]

    m2 = [[2, 0, 0],
          [0, 2, 0],
          [0, 0, 1]]

    m3 = [[1, 0, Q[0]/-100],
          [0, 1, Q[1]/-100],
          [0, 0, 1]]

    t = m_inmultire(m1, m2)
    t = m_inmultire(t, m3)
    t = m_inmultire(t, coord)
    coord = set_new_coords(coord,t)
    return coord

def ex3(coord,Q,V):
    m1 = [[1, 0, Q[0]/100],
          [0, 1, Q[1]/100],
          [0, 0, 1]]

    m2 = [[V[0], 0, 0],
          [0, V[1], 0],
          [0, 0, 1]]

    m3 = [[1, 0, Q[0]/-100],
          [0, 1, Q[1]/-100],
          [0, 0, 1]]

    t = m_inmultire(m1, m2)
    t = m_inmultire(t, m3)
    t = m_inmultire(t, coord)
    coord = set_new_coords(coord,t)
    return coord

def ex4(coord,Q,V,angle):
    value = math.tan(math.radians(angle))
    v1 = V[0]/math.sqrt( math.pow(V[0],2) + math.pow(V[1],2) )
    v2 = V[1]/math.sqrt( math.pow(V[0],2) + math.pow(V[1],2) )
    m1 = [[1-value*v1*v2, value*math.pow(v1,2), -1*value*v1*(v1*Q[1]/100-v2*Q[0]/100)],
          [-1*value*math.pow(v2,2), 1+value*v1*v2, -1*value*v2*(v1*Q[1]/100-v2*Q[0]/100)],
          [0, 0, 1]]

    t = m_inmultire(m1, coord)
    coord = set_new_coords(coord,t)
    return coord

def ex5(coord,Q,V,angle):
    value = math.tan(math.radians(angle))
    v1 = V[0]/math.sqrt( math.pow(V[0],2) + math.pow(V[1],2) )
    v2 = V[1]/math.sqrt( math.pow(V[0],2) + math.pow(V[1],2) )
    m1 = [[1-value*v1*v2, value*math.pow(v1,2), -1*value*v1*(v1*Q[1]/100-v2*Q[0]/100)],
          [-1*value*math.pow(v2,2), 1+value*v1*v2, -1*value*v2*(v1*Q[1]/100-v2*Q[0]/100)],
          [0, 0, 1]]
    t = m_inmultire(m1, coord)
    coord = set_new_coords(coord,t)
    for i in range(len(coord)):
        for j in range(len(coord[i])):
            print(coord[i][j])
    return coord

def main():
    ex = int(input("Numarul exercitiului: "))
    if ex<5:
        coord, res, origine, blank = set_values(1)
    else:
        coord, res, origine, blank = set_values(2)
    str = input(" Dati coord lui Q: ")
    a,b = str.split(' ')
    a = int(a)
    b = int(b)
    Q = [a*100,b*100]

    create_axis(blank,origine,res)
    color = [0,255,0]
    create_polygon(blank,origine,coord,color)

    if ex==1:
        str = input("Dati translatia de vector: ")
        a,b = str.split(' ')
        V = [int(a),int(b)]
        coord = ex1(coord,Q,V)
    elif ex==2:
        coord = ex2(coord,Q)
    elif ex==3:
        str = input("Dati scala: ")
        a,b = str.split(' ')
        V = [int(a),int(b)]
        coord = ex3(coord,Q,V)
    elif ex==4:
        str = input("Dati directia vectorului: ")
        a,b = str.split(' ')
        V = [int(a),int(b)]
        angle = int(input("Dati unghiul: "))
        coord = ex4(coord,Q,V,angle)
    elif ex==5:
        str = input("Dati directia vectorului: ")
        a,b = str.split(' ')
        V = [int(a),int(b)]
        angle = int(input("Dati unghiul: "))
        coord = ex5(coord,Q,V,angle)

    color = [128,0,128]
    create_polygon(blank,origine,coord,color)
    cv.line(blank, (origine[0] + Q[0], origine[1] + Q[1]), (origine[0] + Q[0], origine[1] + Q[1]), (0, 0, 255), 3)

    blank = cv.flip(blank, 0)
    cv.imshow('Deadge', blank)

    cv.waitKey(0)
    cv.destroyAllWindows()

main()
#blank = rotate_image(blank, 180)