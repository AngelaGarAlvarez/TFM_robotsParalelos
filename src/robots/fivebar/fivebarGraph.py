'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from src.robots.fivebar.fivebar import Fivebar
from src.optimization.problems.fivebarProblem import FivebarProblem
import numpy as np
import scipy.spatial as sp

def addRectangle(ax):
	'''
	Add rectangle to determine objective region
	:param ax: subplot where draw the rectangle
	:return:
	'''
	ax.add_patch(Rectangle(
		(robot.center.x - .5*l, + robot.center.y - .5*L),
		l,
		L,
		fill=False,
		color="k",
		zorder=10.,
		hatch='/'))

def generateGraph(x, y, ps, fig, ax, color, title):
	'''
	Generate and save graph
	:param x: list of x coordinates
	:param y: list of y coordinates
	:param ps: special points to draw in other color
	:param fig: figure
	:param ax: subplot where draw
	:param color: color for the speacil points
	:param title: title of the subplot
	'''
	ax.scatter(x, y, color='lightgrey', alpha=0.5)
	ax.set_aspect('equal', 'box')

	im1 = ax.scatter(x, y, c=ps, alpha=0.5, cmap= color)

	c1 = fig.colorbar(im1, ax=ax)
	c1.ax.set_title(title)

	addRectangle(ax)

	ax.set_ylim(min(y), max(y) + 10)

def main():
	global l, L, robot
	l = input("Dimension 1:")
	L = input("Dimension 2:")

	title = str(raw_input("Nombre (enter para nombre por defecto):") or "N")
	l1 = input("Brazo l1:")
	L1 = input("Brazo L1:")
	d = input("Distancia d:")

	if title == "N":
		title = "FIVE-L%.2f-l%.2f-d%.2f" % (L1, l1,d)

	robot = Fivebar(l1, L1, d, 10000)
	points = robot.getWorkspace()
	xs, ys = zip(*[(p.x, p.y) for p in points])
	ss = [p.s for p in points]
	gs = [p.ci for p in points]

	fig = plt.figure()
	ax1 = fig.add_subplot(211)
	ax2 = fig.add_subplot(212)
	fig.canvas.set_window_title(title)
	generateGraph(xs, ys, ss, fig, ax1, 'Greens', '$RI$')
	generateGraph(xs, ys, gs, fig, ax2, 'Blues', '$CI$')
	title = title + ".png"
	fig.tight_layout()

	ax1.get_shared_x_axes().join(ax1, ax2)
	ax1.set_xticklabels([])
	plt.tight_layout()
	fig.suptitle("l=%.2f, L=%.2f, d=%.2f"%(l1,L1,d))
	fig.savefig(title)
	

main()