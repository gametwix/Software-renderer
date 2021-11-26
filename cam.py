import pygame as pg
import numpy as np
import objct
import matrixs

class Camera:
    def __init__(self,screen, height, width):
        self.Pos = np.array([0,0,-30,1])
        self.Right = np.array([1,0,0,0])
        self.Up = np.array([0,1,0,0])
        self.Forward = np.array([0,0,1,0])
        self.Screen = screen
        self.Width = width
        self.Height = height
        self.Angle = np.pi / 3
        self.Focus = (1/np.tan(self.Angle))*self.Width
        #self.Focus = 10000
        self.moving_speed = 2
        self.rotation_speed = 0.1

    def to_cam_matrix(self):
        rx,ry,rz,rw = self.Right
        ux,uy,uz,uw = self.Up
        fx,fy,fz,fw = self.Forward
        return np.array([
            [rx,ux,fx,0],
            [ry,uy,fy,0],
            [rz,uz,fz,0],
            [0,0,0,1]])
    
    def Point_to_cam(self,point):
        rotate_to_cam = self.to_cam_matrix()
        px,py,pz,pw = self.Pos
        
        translate_to_cam = matrixs.translate(-px,-py,-pz)
        point = point @ translate_to_cam
        
        point = point @ rotate_to_cam
        #print(point)
        return point

    def Point_pojection(self,point):
        x,y,z,w = point
        x = (x * self.Focus)/z
        y = (y * self.Focus)/z
        x = self.Width/2 + x
        y = self.Height/2 - y
        return [int(x),int(y)]


    def Draw_polygon(self,points = list(),light = ''):
        point_to_draw = list()
        points_cam = list()
        for point in points:
            p_c = self.Point_to_cam(point) 
            points_cam.append(p_c)
            if(p_c[2] <= 0):
                return
            p_p = self.Point_pojection(p_c)
            point_to_draw.append(p_p)
        p0 = points_cam[0]
        p1 = points_cam[1]
        p2 = points_cam[2]
        v1 = np.array([p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]])
        v2 = np.array([p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]])
        norm = np.cross(v1,v2)
        p0 = np.array([p0[0],p0[1],p0[2]])
        norm = norm / (-np.sqrt(norm.dot(norm)))
        p0 = p0/ np.sqrt(p0.dot(p0))
        if(np.dot(p0,norm) >= 0):
            light = self.Point_to_cam(light)
            light = np.array([light[0],light[1],light[2]])
            light = light / np.sqrt(light.dot(light))
            color = int((255 * np.dot(light,norm) + 255)/2)
            #print(color)
            pg.draw.polygon(self.Screen,pg.Color(color,color,color),point_to_draw,0)
            #pg.draw.polygon(self.Screen,"green",point_to_draw,1)

    def Projection_poligon(self, polygon):
        points_cam = list()
        for point in polygon:
            p_c = self.Point_to_cam(point) 
            points_cam.append(p_c)
            if(p_c[2] <= 0):
                return False
        p0 = points_cam[0]
        p1 = points_cam[1]
        p2 = points_cam[2]
        v1 = np.array([p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]])
        v2 = np.array([p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]])
        norm = np.cross(v1,v2)
        p0 = np.array([p0[0],p0[1],p0[2]])
        norm = norm / (-np.sqrt(norm.dot(norm)))
        p0 = p0/ np.sqrt(p0.dot(p0))
        if(np.dot(p0,norm) >= 0):
            return True
        return False

    def After(self, poligon1 = list()):
        return self.Point_to_cam(poligon1[0])[2]

    def Draw_obj(self,obj,light):
        polygons = list()
        for face in obj.Faces:
            polygon = list()
            for point in face:
                polygon.append(obj.Points[point])
            polygons.append(polygon)
        
        polygons = sorted(polygons ,key = self.After, reverse= True)
                    


        
        for polygon in polygons:
            self.Draw_polygon(polygon,light)

    def Control(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            self.Pos = self.Pos + self.Forward @ matrixs.scale(self.moving_speed)
        if key[pg.K_s]:
            self.Pos = self.Pos - self.Forward @ matrixs.scale(self.moving_speed)
        if key[pg.K_d]:
            self.Pos = self.Pos + self.Right @ matrixs.scale(self.moving_speed)
        if key[pg.K_a]:
            self.Pos = self.Pos - self.Right @ matrixs.scale(self.moving_speed)
        if key[pg.K_LSHIFT]:
            self.Pos = self.Pos - self.Up @ matrixs.scale(self.moving_speed)
        if key[pg.K_SPACE]:
            self.Pos = self.Pos + self.Up @ matrixs.scale(self.moving_speed)
        if key[pg.K_RIGHT]:
            mtocam = self.to_cam_matrix()
            rotate = matrixs.rotate_y(self.rotation_speed) @ np.linalg.inv(mtocam)
            self.Up = np.array([0,1,0,0]) @ rotate 
            self.Right = np.array([1,0,0,0]) @ rotate 
            self.Forward = np.array([0,0,1,0]) @ rotate 
        if key[pg.K_LEFT]:
            mtocam = self.to_cam_matrix()
            rotate = matrixs.rotate_y(-self.rotation_speed) @ np.linalg.inv(mtocam)
            self.Up = np.array([0,1,0,0]) @ rotate 
            self.Right = np.array([1,0,0,0]) @ rotate 
            self.Forward = np.array([0,0,1,0]) @ rotate
        if key[pg.K_UP]:
            mtocam = self.to_cam_matrix()
            rotate = matrixs.rotate_x(-self.rotation_speed) @ np.linalg.inv(mtocam)
            self.Up = np.array([0,1,0,0]) @ rotate 
            self.Right = np.array([1,0,0,0]) @ rotate
            self.Forward = np.array([0,0,1,0]) @ rotate 
        if key[pg.K_DOWN]:
            mtocam = self.to_cam_matrix()
            rotate = matrixs.rotate_x(self.rotation_speed) @ np.linalg.inv(mtocam)
            self.Up = np.array([0,1,0,0]) @ rotate 
            self.Right = np.array([1,0,0,0]) @ rotate 
            self.Forward = np.array([0,0,1,0]) @ rotate 

