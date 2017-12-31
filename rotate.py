import os
import numpy as np

step = 90
meshname='Wolf'
directory = meshname + "-rotated-" + str(step)

if( (360%step )!=0):
    raise ValueError('Step value error.')


oriobj = open(meshname+".obj", "r")

if not os.path.exists(directory):
    os.makedirs(directory)

for x in range(0, 360, step):

    thetax = np.radians(x)
    cx, sx = np.cos(thetax), np.sin(thetax)
    rx = np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(1, 0, 0, 0, cx, sx, 0, -sx, cx))

    for y in range(0, 360, step):
        thetay = np.radians(y)
        cy, sy = np.cos(thetay), np.sin(thetay)
        ry = np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(cy, 0, -sy, 0, 1, 0, sy, 0, cy))

        for z in range(0, 360, step):

            thetaz = np.radians(z)
            cz, sz = np.cos(thetaz), np.sin(thetaz)
            rz = np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(cz, sz, 0, -sz, cz, 0, 0, 0, 1))

            filename = directory + "/" + meshname + "-" + str(x) + "-" + str(y) + "-" + str(z) + '.obj'
            f = open(filename, 'w')

            for line in oriobj:
                if line[:2] == 'v ':
                    na = np.fromstring(line[2:], dtype=np.float, sep=' ')
                    if na!=[]:
                        na = np.dot(na, rx)
                        na = np.dot(na, ry)
                        na = np.dot(na, rz)
                        nl = "v {} {} {}".format(na.item(0), na.item(1), na.item(2))
                        f.write(nl + "\n")
                elif line[:3] == 'vt ':
                    na = np.fromstring(line[2:], dtype=np.float, sep=' ')
                    if na!=[]:
                        na = np.dot(na, rx)
                        na = np.dot(na, ry)
                        na = np.dot(na, rz)
                        nl = "vt {} {} {}".format(na.item(0), na.item(1), na.item(2))
                        f.write(nl + "\n")
                else:
                    if line[:6] != "usemtl":
                        f.write(line)
            oriobj.seek(0)
