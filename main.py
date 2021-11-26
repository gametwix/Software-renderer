import pygame as pg
import numpy as np
import objct
import cam
import matrixs

class Program:
    def __init__(self):
        pg.init()
        self.RES =  self.WIDTH, self.HEIGHT = 1600, 900
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.camera = cam.Camera(self.screen,self.HEIGHT,self.WIDTH)
        pg.display.set_caption('Main')
        

    def draw(self):
        self.screen.fill('azure3')
        

    def run(self):
        ob1 = objct.Object()
        ob1.obj_to_Object('tiapot.obj')
        sc = matrixs.scale(1)
        for i in range(len(ob1.Points)):
            ob1.Points[i] = ob1.Points[i] @ sc
        print(ob1.Points)
        light = np.array([20,-20,20,1])
        a = 0.05
        r_x = matrixs.rotate_x(a)
        r_y = matrixs.rotate_y(a)
        r_z = matrixs.rotate_z(a)
        while True:
            light = light @ r_x @ r_y @ r_z
            self.camera.Control()
            self.draw()
            self.camera.Draw_obj(ob1,light)
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    pr = Program()
    pr.run()