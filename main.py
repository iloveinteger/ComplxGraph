from flask import Flask, request, render_template
import math
import cv2
from colorsys import hsv_to_rgb
import os

# Get the absolute path of the directory where this script is located
dir_path = os.path.dirname(os.path.realpath(__file__))

# Change the current working directory to the script's directory
os.chdir(dir_path)


app = Flask(__name__)

o = (2500,2500)
graph1 = cv2.imread("empty.png")

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.func = "z"

    def setPoint(self,x,y):
        self.x = x
        self.y = y
        self.r = (self.x**2 + self.y**2)**(1/2)
        self.a = math.atan2(self.y,self.x)
        if self.a<0:
            self.a = 2*math.pi + self.a

    def calcPoint(self,func):
        self.z = complex(self.x,self.y)
        self.outz = eval(func.replace("z","("+str(self.z)+")"))

    def colorPoint(self):
        self.h = (self.a/math.pi*180)/360
        self.s = 1
        if self.r==0:
            self.v = 0
        else:
            self.v = self.r**1.5/(1+self.r**1.5)
        return tuple(map(lambda x : x*255, hsv_to_rgb(self.h,self.s,self.v)))

def drawf(func):
    for x in range(-2500,2505,10):
        for y in range(-2500,2505,10):
            z0 = Point()
            z0.setPoint(x,y)
            z0.calcPoint(func)
            f = Point()
            f.setPoint(z0.outz.real,z0.outz.imag)
            xy = (x+o[0],-y+o[1])
            cv2.line(graph1,xy,xy,f.colorPoint(),thickness=12)
    
    resized_graph = cv2.resize(graph1, (0, 0), fx=0.1, fy=0.1)

    cv2.imwrite("static/graph1.png",resized_graph)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        func = request.form['function']
        try:
            drawf(func)
            return render_template('index.html', image_file="graph1.png")
        except Exception as e:
            print("An error occurred:", e)
            return render_template('index.html', image_file="error.png")
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
