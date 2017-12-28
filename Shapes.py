# CS5 Black, hw10pr2
# Filename: shapes.py
# File Writer: RLH January 26, 2010
# Problem description: Shape class and friends

import math
import turtle

from Matrix import *
from Vector import *

class Shape(object):
    def __init__(self):
        self.points = []
        
    def render(self):
        """Use turtle graphics to render shape"""
        turtle.penup()
        turtle.setposition(self.points[0].x, self.points[0].y)
        turtle.pendown()
        turtle.fillcolor(self.color)
        turtle.pencolor(self.color)
        turtle.begin_fill()
        for vector in self.points[1:]:
            turtle.setposition(vector.x, vector.y)
        turtle.setposition(self.points[0].x, self.points[0].y)
        turtle.end_fill()

    def erase(self):
        """Draw shape in white to effectively erase it from screen"""
        temp = self.color
        self.color = "white"
        self.render()
        self.color = temp
    
    def rotate(self, theta,rotateAbout= Vector(0,0)):
        """Rotate shape by theta degrees """
        self.translate(Vector(-rotateAbout.x, -rotateAbout.y))
        theta = math.radians(theta)  # THIS IS CORRECT!
        # Python's trig functions expect input in radians
        # so this function converts from degrees into radians.
        RotationMatrix = Matrix(math.cos(theta), -1*math.sin(theta), math.sin(theta), math.cos(theta))
        NewPoints = []
        for vector in self.points:
            newvector = RotationMatrix * vector
            NewPoints.append(newvector)
        self.points = NewPoints
        self.center= RotationMatrix * self.center
        self.translate(rotateAbout)
        
        
    def translate(self,vec):
        """translates all the points of a given object self by a vector vec
        """
        NewPoints = []
        for point in self.points:
            newpoint = Vector(point.x + vec.x, point.y + vec.y)
            NewPoints.append(newpoint)
        self.points = NewPoints
        self.center= self.center + vec
    
    def scale(self, s):
        """ scales a current shape by a factor of s
        """
        scalematrix = Matrix(s,0,0,s)
        c = self.center
        self.translate(Vector(-c.x,-c.y))
        NewPoints= []
        for vec in self.points:
            newvec = scalematrix * vec
            NewPoints.append(newvec)
        self.points = NewPoints
        self.translate(c)
    
    def flip(self,v1,v2):
        """flips an object around a given line 
        this line is defined by two input vectors
        """
        slope = (v2.y-v1.y)/ (v2.x-v1.x)
        theta = math.atan(slope)
        theta = math.degrees(theta)
        self.rotate(-theta,v1)
        self.translate(-v1)
        NewPoints=[]
        for vec in self.points:
            newvec = Vector(vec.x,-vec.y)
            NewPoints.append(newvec)
        self.points = NewPoints
        self.translate(v1)
        self.rotate(theta,v1)
        self.center= Vector((self.points[0].x+self.points[3].x)/2,(self.points[0].y+self.points[1].y)/2 )

class Rectangle(Shape):
    def __init__(self, width, height, center = Vector(0, 0), color = "black"):
        SW = Vector(center.x - width/2.0, center.y - height/2.0)
        NW = Vector(center.x - width/2.0, center.y + height/2.0)
        NE = Vector(center.x + width/2.0, center.y + height/2.0)
        SE = Vector(center.x + width/2.0, center.y - height/2.0)
        self.points = [SW, NW, NE, SE]
        self.color = color
        self.center = center

class Square(Rectangle):
    def __init__(self, width, center=Vector(0, 0), color = "black"):
        Rectangle.__init__(self, width, width, center, color)
        
class Circle(Shape):
    def __init__(self, center = Vector(0, 0), radius = 10, color = "black"):
        self.center = center
        self.radius = radius
        self.color = color

    def render(self):
        turtle.penup()
        turtle.setposition(self.center.x, self.center.y-self.radius)
        turtle.pendown()
        turtle.fillcolor(self.color)
        turtle.pencolor(self.color)
        turtle.begin_fill()
        turtle.circle(self.radius)
        turtle.end_fill()

    def rotate(self, theta, rotateAbout= Vector(0,0)):
        """ theta is in degrees """
        self.translate(Vector(-rotateAbout.x, -rotateAbout.y))
        theta = math.radians(theta)
        RotationMatrix = Matrix(math.cos(theta), -1*math.sin(theta), math.sin(theta), math.cos(theta))        
        self.center = RotationMatrix * self.center
        self.translate(rotateAbout)
        

    def scale(self, s):
        """ scales a current shapes by a factor of s
        """
        self.radius = s * self.radius

    def translate(self,vec):
        """ moves the circle by a vector vec
        """
        self.center = Vector(self.center.x + vec.x , self.center.y + vec.y)

    def flip(self,v1,v2):
        slope = (v2.y-v1.y)/ (v2.x-v1.x)
        theta = math.atan(slope)
        theta = math.degrees(theta)
        self.rotate(-theta,v1)
        self.translate(-v1)
        self.center = Vector(self.center.x,-self.center.y)
        self.translate(v1)
        self.rotate(theta,v1)

class Triangle(Shape):
    def __init__(self, p1, p2 , p3, color="black"):
        """ constructer function of a triangle
            inputs of the funtion are three vetors representing the three vertices of the triangle
        """
        point1 = Vector(p1.x,p1.y)
        point2 = Vector(p2.x,p2.y)
        point3 = Vector(p3.x,p3.y)
        self.center = Vector(((p1.x+p2.x+p3.x)/3), ((p1.y+p2.y+p3.y)/3))
        self.points = [point1,point2,point3]
        self.color = color
        
    def flip(self,v1,v2):
        """ flips a given shape around the line segment defined by two vectors V1 and V2
        """
        slope = (v2.y-v1.y)/ (v2.x-v1.x)
        theta = math.atan(slope)
        theta = math.degrees(theta)
        self.rotate(-theta,v1)
        self.translate(-v1)
        NewPoints=[]
        for vec in self.points:
            newvec = Vector(vec.x,-vec.y)
            NewPoints.append(newvec)
        self.points = NewPoints
        self.translate(v1)
        self.rotate(theta,v1)
        self.center = Vector(((self.points[0].x+self.points[1].x+ self.points[2].x)/3), ((self.points[0].y+self.points[1].y+ self.points[2].y)/3))
        
    

class LineSegment(Shape):
    def __init__(self,v1= Vector(0,0),v2=Vector(10,10),color="black"):
        """ Linesegment constructer
        """
        self.points = [v1,v2]
        self.center = Vector((v1.x+v2.x)/2,(v1.y+v2.y)/2)
        self.color=color
    
