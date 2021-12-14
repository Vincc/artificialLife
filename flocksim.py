import pyglet
from pyglet import _thread_trace_func, shapes
import random
import math

from pyglet.graphics import draw

window = pyglet.window.Window()
batch = pyglet.graphics.Batch()
boids = []
size = 100
population = 10

coherence = 0.5
seperation = 3
alignment = 0.1
visualRange = 10

def initBoids():
    for i in range(population):
        #x y dx dy 
        boids.append([size*random.random(), size*random.random(), 0,0])
        
def steervector(body, targetx, targety, turnrate):
    body[2] += (targetx-body[2])*turnrate
    body[3] += (targety-body[3])*turnrate

def distance(b1,b2):
    return math.sqrt((b1[0]-b2[0])**2 + (b1[1]-b2[1])**2)

def update(currentboid):
    #list of boids within visual range
    boids.remove(currentboid)
    active = []
    for i in boids:
        if distance(i,currentboid) < visualRange:
            active.append(i)

    #steer towards center of mass 
    targetxpos = (sum([i[0] for i in active])/len(active))-currentboid[0]
    targetypos = (sum([i[1] for i in active])/len(active))-currentboid[1]
    steervector(currentboid, targetxpos,targetypos,coherence)

    #avoid other boids
    for i in active:
        if distance(i,currentboid) < seperation:
            targetxpos = currentboid[0]-i[0]
            targetypos = currentboid[1]-i[1]
            steervector(currentboid, targetxpos,targetypos,coherence)
            

    #align with other boids accounting for alignment
    targetxvector = sum([i[2] for i in active])/len(active)
    targetyvector = sum([i[3] for i in active])/len(active)
    steervector(currentboid, targetxvector,targetyvector,alignment)

    currentboid[0]+=currentboid[2]
    currentboid[1]+=currentboid[3]
initBoids()

#(item for sublist in [[i[0],i[1]] for i in boids] for item in sublist)

@window.event
def on_draw():
    window.clear()
    drawboid = [int(item) for sublist in [[i[0],i[1]] for i in boids] for item in sublist]
    print(len(drawboid))
    pyglet.graphics.draw(population, pyglet.gl.GL_POINTS,
    ('v2i', drawboid))
"""
def main():
    window = pyglet.window.Window()
    batch = pyglet.graphics.Batch()
    boids = []
    size = 100
    population = 10

    coherence = 0.5
    seperation = 3
    alignment = 0.1
    visualRange = 10

    pyglet.clock.schedule_interval(foo, 1.0)
    pyglet.app.run()
main()"""