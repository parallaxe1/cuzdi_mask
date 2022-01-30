#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 18:02:25 2015

@author: a.mester
"""

#import numpy
import math
import string


def m2pt( m_value ):
    "meter to pt"
    #m2pt = 2.835270768e3*m_value
    m2pt = 1e3 * m_value  # m2mm - update 2020
    return m2pt



def deg2rad( deg_value ):
    "degree to radiant"
    deg2rad = deg_value/180*math.pi
    return deg2rad


def frange(start, stop, step):
    r = start
    xlist = []
    ii = 0
    while (r + ii * step) <= stop:
        xlist.append(r + ii * step)
        ii += 1
    return xlist

def create_svg(conf):


    mittelpunkt = conf.diameter/2
    rand = (conf.diameter-conf.apperture)/2
    slit_sep = conf.slit_width*conf.slit_sep_factor

    file = open('mask.svg', 'w')
    header_svg = open('header_svg.txt', 'r')
    file.write(header_svg.read())
    header_svg.close()
    file.write('<circle cx="{2:5.3f}" cy="{3:5.3f}" r="{0:5.3f}" fill="none" stroke="#0000ff" stroke-width="{1:5.3f}" />\n'.format(
            m2pt(conf.apperture / 2 + rand), m2pt(conf.stroke_width), m2pt(mittelpunkt), m2pt(mittelpunkt)))



    # q1 + q4
    file.write(
        '<rect width="{0:5.3f}" height="{4:5.3f}" rx="{1:5.3f}" ry="{1:5.3f}" x="{2:5.3f}" y="{3:5.3f}" transform="rotate(0 0 0)" id="rect4763-1" style="color:#000000;fill:none;stroke:#0000ff;stroke-width:{5:5.3f};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />\n'.format(
            m2pt(conf.slit_width), m2pt(conf.slit_width / 2), m2pt(mittelpunkt - conf.slit_width / 2), m2pt(rand),
            m2pt(conf.apperture / 2 - conf.sep_horizontal / 2), m2pt(conf.stroke_width)))
    xlist = frange(slit_sep, conf.apperture / 2, slit_sep)
    for (ix) in range(0, len(xlist)):
        height2 = (conf.apperture / 2) ** 2 - xlist[ix] ** 2
        if height2 > 0:
            height = math.sqrt(height2)
            file.write(
                '<rect width="{0:5.3f}" height="{4:5.3f}" rx="{1:5.3f}" ry="{1:5.3f}" x="{2:5.3f}" y="{3:5.3f}" transform="rotate(0 0 0)" id="rect4763-1" style="color:#000000;fill:none;stroke:#0000ff;stroke-width:{5:5.3f};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />\n'.format(
                    m2pt(conf.slit_width), m2pt(conf.slit_width / 2), m2pt(mittelpunkt + xlist[ix] - conf.slit_width / 2),
                    m2pt(rand + conf.apperture / 2 - height), m2pt(height - conf.sep_horizontal / 2), m2pt(conf.stroke_width)))
            file.write(
                '<rect width="{0:5.3f}" height="{4:5.3f}" rx="{1:5.3f}" ry="{1:5.3f}" x="{2:5.3f}" y="{3:5.3f}" transform="rotate(0 0 0)" id="rect4763-1" style="color:#000000;fill:none;stroke:#0000ff;stroke-width:{5:5.3f};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />\n'.format(
                    m2pt(conf.slit_width), m2pt(conf.slit_width / 2), m2pt(mittelpunkt - xlist[ix] - conf.slit_width / 2),
                    m2pt(rand + conf.apperture / 2 - height), m2pt(height - conf.sep_horizontal / 2), m2pt(conf.stroke_width)))

    # q2


    spaltabstand_x = slit_sep / math.cos(deg2rad(conf.slit_angle_q2))
    xlist = frange(conf.sep_vertical / 2, conf.apperture / 2, spaltabstand_x)
    # horizontal
    for (ix) in range(0, len(xlist)):
        a = xlist[ix]
        b = conf.sep_horizontal / 2
        r = conf.apperture / 2
        beta = 90 - conf.slit_angle_q2
        p = 2 * b * math.sin(deg2rad(beta)) + 2 * a * math.cos(deg2rad(beta))
        q = (a ** 2 + b ** 2 - r ** 2)
        h1 = -p / 2 + math.sqrt((p / 2) ** 2 - q)
        h2 = -p / 2 - math.sqrt((p / 2) ** 2 - q)
        h = max(h1, h2)
        # print(h)
        if h > 0:
            # print('s')
            file.write(
                '<rect width="{0:5.3f}" height="{4:5.3f}" rx="{1:5.3f}" ry="{1:5.3f}" x="{2:5.3f}" y="{3:5.3f}" transform="rotate({6:5.3f} {7:5.3f} {8:5.3f})" id="rect4763-1" style="color:#000000;fill:none;stroke:#0000ff;stroke-width:{5:5.3f};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />\n'.format(
                    m2pt(conf.slit_width), m2pt(conf.slit_width / 2), m2pt(mittelpunkt + a - conf.slit_width / 2),
                    m2pt(mittelpunkt + b - conf.slit_width / 2), m2pt(h), m2pt(conf.stroke_width), (-conf.slit_angle_q2),
                    m2pt(mittelpunkt + a), m2pt(mittelpunkt + b)))
    # vertikal
    spaltabstand_y = slit_sep / math.sin(deg2rad(conf.slit_angle_q2))
    ylist = frange(conf.sep_horizontal / 2 + spaltabstand_y, conf.apperture / 2, spaltabstand_y)
    for (iy) in range(0, len(ylist)):
        a = conf.sep_vertical / 2
        b = ylist[iy]
        r = conf.apperture / 2
        beta = 90 - conf.slit_angle_q2
        p = 2 * b * math.sin(deg2rad(beta)) + 2 * a * math.cos(deg2rad(beta))
        q = (a ** 2 + b ** 2 - r ** 2)
        if (p / 2) ** 2 - q > 0:
            h1 = -p / 2 + math.sqrt((p / 2) ** 2 - q)
            h2 = -p / 2 - math.sqrt((p / 2) ** 2 - q)
        else:
            h1 = -p / 2 + math.sqrt(q - (p / 2) ** 2)
            h2 = -p / 2 - math.sqrt(q - (p / 2) ** 2)
        h = max(h1, h2)
        # print(h)
        if h > 0:
            file.write(
                '<rect width="{0:5.3f}" height="{4:5.3f}" rx="{1:5.3f}" ry="{1:5.3f}" x="{2:5.3f}" y="{3:5.3f}" transform="rotate({6:5.3f} {7:5.3f} {8:5.3f})" id="rect4763-1" style="color:#000000;fill:none;stroke:#0000ff;stroke-width:{5:5.3f};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />\n'.format(
                    m2pt(conf.slit_width), m2pt(conf.slit_width / 2), m2pt(mittelpunkt + a - conf.slit_width / 2),
                    m2pt(mittelpunkt + b - conf.slit_width / 2), m2pt(h), m2pt(conf.stroke_width), (-conf.slit_angle_q2),
                    m2pt(mittelpunkt + a), m2pt(mittelpunkt + b)))

    # q3
    spaltabstand_x = slit_sep / math.cos(deg2rad(conf.slit_angle_q3))
    xlist = frange(conf.sep_vertical / 2, conf.apperture / 2, spaltabstand_x)
    # horizontal
    for (ix) in range(0, len(xlist)):
        a = xlist[ix]
        b = conf.sep_horizontal / 2
        r = conf.apperture / 2
        beta = 90 - conf.slit_angle_q3
        p = 2 * b * math.sin(deg2rad(beta)) + 2 * a * math.cos(deg2rad(beta))
        q = (a ** 2 + b ** 2 - r ** 2)
        h1 = -p / 2 + math.sqrt((p / 2) ** 2 - q)
        h2 = -p / 2 - math.sqrt((p / 2) ** 2 - q)
        h = max(h1, h2)
        # print(h)
        if h > 0:
            # print('s')
            file.write(
                '<rect width="{0:5.3f}" height="{4:5.3f}" rx="{1:5.3f}" ry="{1:5.3f}" x="{2:5.3f}" y="{3:5.3f}" transform="rotate({6:5.3f} {7:5.3f} {8:5.3f})" id="rect4763-1" style="color:#000000;fill:none;stroke:#0000ff;stroke-width:{5:5.3f};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />\n'.format(
                    m2pt(conf.slit_width), m2pt(conf.slit_width / 2), m2pt(mittelpunkt - a - conf.slit_width / 2),
                    m2pt(mittelpunkt + b - conf.slit_width / 2), m2pt(h), m2pt(conf.stroke_width), (conf.slit_angle_q3), m2pt(mittelpunkt - a),
                    m2pt(mittelpunkt + b)))
    # vertikal
    spaltabstand_y = slit_sep / math.sin(deg2rad(conf.slit_angle_q3))
    ylist = frange(conf.sep_horizontal / 2 + spaltabstand_y, conf.apperture / 2, spaltabstand_y)
    for (iy) in range(0, len(ylist)):
        a = conf.sep_vertical / 2
        b = ylist[iy]
        r = conf.apperture / 2
        beta = 90 - conf.slit_angle_q3
        p = 2 * b * math.sin(deg2rad(beta)) + 2 * a * math.cos(deg2rad(beta))
        q = (a ** 2 + b ** 2 - r ** 2)
        if (p / 2) ** 2 - q > 0:
            h1 = -p / 2 + math.sqrt((p / 2) ** 2 - q)
            h2 = -p / 2 - math.sqrt((p / 2) ** 2 - q)
        else:
            h1 = -p / 2 + math.sqrt(q - (p / 2) ** 2)
            h2 = -p / 2 - math.sqrt(q - (p / 2) ** 2)
        h = max(h1, h2)
        # print(h)
        if h > 0:
            file.write(
                '<rect width="{0:5.3f}" height="{4:5.3f}" rx="{1:5.3f}" ry="{1:5.3f}" x="{2:5.3f}" y="{3:5.3f}" transform="rotate({6:5.3f} {7:5.3f} {8:5.3f})" id="rect4763-1" style="color:#000000;fill:none;stroke:#0000ff;stroke-width:{5:5.3f};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />\n'.format(
                    m2pt(conf.slit_width), m2pt(conf.slit_width / 2), m2pt(mittelpunkt - a - conf.slit_width / 2),
                    m2pt(mittelpunkt + b - conf.slit_width / 2), m2pt(h), m2pt(conf.stroke_width), (conf.slit_angle_q3), m2pt(mittelpunkt - a),
                    m2pt(mittelpunkt + b)))
        file.write('</svg>\n')
    file.close()

def calc_slit_width(conf):
    conf.store_slit_width(conf.wavelength/math.sin(conf.pixel_size/conf.focal_length*conf.num_pixel))
    print('Spaltbreite / mm: '+str(round(conf.slit_width*1000,3))+'')

    slit_sep = conf.slit_width*conf.slit_sep_factor

    I_0 = 1;

    pixels = frange(-(conf.num_pixel/2),(conf.num_pixel/2),0.1)
    temp = conf.pixel_size/conf.focal_length

    alpha = [x*temp for x in pixels]

    # Einzelspalt
    temp = math.pi*conf.slit_width/conf.wavelength
    phi_ss = [temp*math.sin(x) for x in alpha]
    # zur besseren rechnung division durch null vermeiden:
    phi_ss[int(round(len(phi_ss)/2))] = 1.0
    I_ss = [I_0*(math.sin(x)/(x))**2 for x in phi_ss]


    # Gitter
    temp = math.pi*slit_sep/conf.wavelength
    phi_ms = [temp*math.sin(x) for x in alpha]
    # zur besseren rechnung division durch null vermeiden:
    phi_ms[int(round(len(phi_ms)/2))] = 1.0
    N = round(conf.apperture/slit_sep) #Anzahl spalte - Mehr Spalte machen schmallere Einzel-Peaks
    print('Anzahl Spalte in der oberen Hälfte der Maske (circa): '+str(N)+'')
    I_ms = [I_0*(math.sin(N*x)/(N*math.sin(x)))**2 for x in phi_ms]


    id = 0
    #[a*b for a,b in zip(lista,listb)]
    data = [x*y for x,y in zip(I_ms,I_ss)]
    data0 = ""
    for (ii) in frange(1,len(pixels)-10,10):
        if(max(data[ii:ii+10]) > 0.5 and max(data[ii:ii+10]) < 0.8):
            data0 += "+"
        elif(max(data[ii:ii+10]) > 0.8):
            data0 += "#"
        else:
            data0 += "."
        #pixels0[id] = mean(pixels(ii:ii+9));
        id = id+1

    temp = list(data0)
    temp[int(round(len(temp)/2))-1] = "#"
    data0 = "".join(temp)
    print('Abbildung der Interferenzmuster auf dem Kamera-Chip:')
    print(data0+'\n')

    print('Die Abbildung gibt nur das Interferenzmuster wieder, welches von der oberen Hälfte der Maske hervorgerufen wird. Die beiden unteren Quadranten ergeben ein etwas gröberes Muster, da sie weniger Spalte enthalten. Ein Zeichen entspricht einem Pixel.')
    print('".": Helligkeit kleiner als 50% vom Maximalwert (Zentrum).')
    print('"+": Helligkeit größer als 50% vom Maximalwert (Zentrum).')
    print('"#": Helligkeit größer als 80% vom Maximalwert (Zentrum).')

    return conf

