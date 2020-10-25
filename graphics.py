from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Line, Color
import numpy as np
import time
from kivy.core.window import Window
import os


class Spiral(Widget):
    i = 0
    event = Clock.schedule_interval
    t = 1/60.
    k = 1
    g = 0.2
    pathfile = str()
    folderpath = str()
    timing = 0
    points = []
    frames = 1025
    path = str()
    touch = []



    def generate_spiral(self, i, path):
        self.path = path
        if len(self.points) != self.frames:
            if i % 2 == 0:
                self.k = self.k * 1.001
            i = i * self.k
            t = i * self.g

            # x, y данные на графике
            x = t * np.sin(t / 18)
            y = t * np.cos(t / 18)

            with open(os.path.join(self.path, str(Window.width) + '_' + str(Window.height) + '.csv'), 'a') as ouf:
                    ouf.write(str(Window.width / 2 + x)+','+str(Window.height / 2 + y)+'\n')


    def readfromfile(self):
        if len(self.points) < self.frames-1:
            try:
                x = []
                self.points = []
                with open(os.path.join(self.path, str(Window.width) + '_' + str(Window.height) + '.csv'), 'r') as ouf:
                    for line in ouf:
                        x.append([float(p) for p in line.split(',')])
                        if len(x) == self.frames:
                            break
                self.points = x
                if len(self.points) >= self.frames-1:
                    return True
                else:
                    return False
            except FileNotFoundError:
                return False
        else:
            return True


    def clr(self):
        self.canvas.clear()

    def reload(self):
        self.i = 0
        self.t = 0.00001
        self.k = 1
        self.g = 0.2
    
    
    def on_touch_down(self, touch):
        color = (0, 0, 0, 1)
        with self.canvas:
            Color(*color, mode='rgba')
            touch.ud['line'] = Line(points=(touch.x, touch.y))
            self.touch.append([])
            self.touch.append([])
            self.touch.append([(time.time() - self.timing), touch.x, touch.y])
            print(self.touch)
            with open(self.pathfile, 'a') as ouf:
                ouf.write('\n')
                ouf.write('\n')
                ouf.write(str(time.time() - self.timing)+','+str(touch.x)+','+str(touch.y)+'\n')
    
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
        print(touch.ud['line'].points)
        self.touch.append([(time.time() - self.timing), touch.x, touch.y])
        print(self.touch)
        with open(self.pathfile, 'a') as ouf:
            ouf.write(str(time.time() - self.timing)+','+str(touch.x) + ',' + str(touch.y)+'\n')
        return touch.ud['line'].points

    # def save_to_file(self):
    #     with open(self.pathfile, 'a') as ouf:
    #         for i in self.touch:
    #             print(len(i))
    #             if len(i) > 0:
    #                 ouf.write(str(i[0])+','+str(i[1]) + ',' + str(i[2])+'\n')
    #             else:
    #                 ouf.write('\n')


    def static_spiral(self, width = 10):
        self.timing = time.time()
        n = len(self.points)
        x = []
        with self.canvas:
            Color(236 / 255, 129 / 255, 47 / 255)
            Line(points=self.points[2:n], width=width)
        with self.canvas:
            Color(63 / 255, 125 / 255, 245 / 255)
            Line(points=self.points[0:2], width=width)
        with self.canvas:
            Color(255 / 255, 63 / 255, 63 / 255)
            x.append(self.points[-1])
            x.append(self.points[-1])
            Line(points=x, width=width)



class Two_Spiral(Widget):
    i = 0
    event = Clock.schedule_interval
    t = 1 / 60.
    k = 1
    g = 0.2
    pathfile = str()
    folderpath = str()
    timing = 0
    points_two_spiral = []
    frames_two_spiral = 675
    path = str()


    def clr(self):
        self.canvas.clear()

    def reload(self):
        self.i = 0
        self.t = 0.00001
        self.k = 1
        self.g = 0.2

    def generate_two_spiral(self, i, path):
        self.path = path
        height = Window.height - (Window.height / 10 + Window.height / 15 + 15)
        height = height/4 + Window.height / 15 + 15
        if len(self.points_two_spiral) != self.frames_two_spiral:
            if i % 2 == 0:
                self.k = self.k * 1.001
            i = i * self.k
            t = i * self.g

            # x, y данные на графике
            x = t * np.sin(t / 10)
            y = t * np.cos(t / 10)

            with open(os.path.join(self.path, 'two_spiral_' + str(Window.width) + '_' + str(Window.height) + '.csv'),
                      'a') as ouf:
                ouf.write(str(Window.width / 2 + x) + ',' + str(height + y) + '\n')

    def readfromfile_two_spiral(self):
        try:
            x = []
            self.points_two_spiral = []
            with open(
                    os.path.join(self.path, 'two_spiral_' + str(Window.width) + '_' + str(Window.height) + '.csv'),
                    'r') as ouf:
                for line in ouf:
                    x.append([float(p) for p in line.split(',')])
                    if len(x) == self.frames_two_spiral:
                        break
            self.points_two_spiral = x
            if len(self.points_two_spiral) >= self.frames_two_spiral - 1:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def two_spiral(self, width=10):
        self.timing = time.time()
        n = len(self.points_two_spiral)
        height = Window.height - (Window.height / 10 + Window.height / 15 + 15)
        x = []
        # with self.canvas:
        #     Color(236 / 255, 129 / 255, 47 / 255)
        #     Line(points=self.points_two_spiral[2:n], width=10)
        with self.canvas:
            Color(63 / 255, 125 / 255, 245 / 255)
            Line(points=self.points_two_spiral[0:2], width=width)
        # with self.canvas:
        #     Color(255 / 255, 63 / 255, 63 / 255)
        #     x.append(self.points_two_spiral[-1])
        #     x.append(self.points_two_spiral[-1])
        #     print(x)
        #     Line(points=x, width=10)

        for h in range(n):
            self.points_two_spiral[h][1] = self.points_two_spiral[h][1] + height / 2
        with self.canvas:
            Color(236 / 255, 129 / 255, 47 / 255)
            Line(points=self.points_two_spiral[0:n], width=width)

    def on_touch_down(self, touch):
        color = (0, 0, 0, 1)
        with self.canvas:
            Color(*color, mode='rgba')
            touch.ud['line'] = Line(points=(touch.x, touch.y))
            with open(self.pathfile, 'a') as ouf:
                ouf.write('\n')
                ouf.write('\n')
                ouf.write(str(time.time() - self.timing) + ',' + str(touch.x) + ',' + str(touch.y) + '\n')

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
        print(touch.ud['line'].points)
        with open(self.pathfile, 'a') as ouf:
            ouf.write(str(time.time() - self.timing) + ',' + str(touch.x) + ',' + str(touch.y) + '\n')
        return touch.ud['line'].points
