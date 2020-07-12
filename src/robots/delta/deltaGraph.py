'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as Rect
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import *
from scipy.spatial import *
import scipy.spatial as sp
from src.robots.delta.delta import Delta
import os.path

global robot

def getCubelines(robot, ao, go, ho):
	'''
	Get cubelines to draw objective region
	:param robot: manipulator to obtains it workspace center
	:param a: width of the objective region
	:param g: depth of the objective region
	:param h: height of the objectve region
	:return: cubelines to draw the  prism
	'''
	# calculando vertices del prisma
	ps = (ao * .5 , go * .5, ho *.5)
	# calculando lineas para dibujar el cubo
	r1, r2, r3 = [p for p in [(-1 * ps[i] + robot.center.dims[i],
							   1 * ps[i] + robot.center.dims[i]) for i in (0, 1, 2)]]
	cubelines = []
	for s, e in combinations(np.array(list(product(r1, r2, r3))), 2):
		if np.sum(np.abs(s - e)) == r1[1] - r1[0] or np.sum(np.abs(s - e)) == r2[1] - r2[0]\
				or np.sum(np.abs(s - e)) == r3[1] - r3[0]: cubelines.append(zip(s, e))
	return cubelines

def workspaceToDraw(points):
	'''
	Workspace points to draw
	:param points: points of the workspace to draw
	:return: Convex Hull to draw correctly the workspace
	'''
	points = np.array(points)
	hull = sp.ConvexHull(points=points, incremental = True)
	return [[points[S, 0], points[S, 1], points[S, 2]] for S in hull.simplices]

def graph3d(robot, title, L1, l1, b, pr, ao, go, ho):
	'''
	Generate and save graph of the workspace in 3D
	:pa
	:param title: title of the graph
	:param L1: largest linkage of the manipulator
	:param l1: smallest  linkage of the manipulator
    :param b: distane brom center to linkages in the base
    :param pr: distane brom center to linkages in the efector
	:param ao: width of the objective region
	:param go: depth of the objective region
	:param ho: height of the objectve region
	'''
	fig = plt.figure(figsize=(8, 6))
	fig.canvas.set_window_title(title)
	ax1 = fig.add_subplot(121, projection=Axes3D.name)
	ax2 = fig.add_subplot(122, projection=Axes3D.name)
	cubelines = getCubelines(robot, ao, go, ho)

	res = workspaceToDraw(points)
	xs, ys, zs = zip(*points)
	[ax1.plot_trisurf(r[0], r[1], r[2],
					  alpha=0.4, antialiased=True, color='lightgrey') for r in res]
	[ax2.plot_trisurf(r[0], r[1], r[2],
					  alpha=0.4, antialiased=True, color='lightgrey') for r in res]

	[ax1.plot(*c, color='k') for c in cubelines]
	[ax2.plot(*c, color='k') for c in cubelines]

	ax1.set_aspect('equal', 'box')
	ax2.set_aspect('equal', 'box')

	ax1.scatter(xs, ys, zs, c=ss, alpha=0.05, cmap='Greens')
	ax2.scatter(xs, ys, zs, c=gs, alpha=0.05, cmap='Blues')

	title = title.replace(" ", "") + "-3d.png"
	plt.tight_layout()
	fig.suptitle("l=%.2f, L=%.2f, b=%.2f, p=%.2f"%(l1,L1,b,pr))
	fig.savefig(title)

def procesGraph(ax, a1, a2, values, colors):
	ax.scatter(a1, a2, c='lightgrey', alpha=0.5)
	im = ax.scatter(a1, a2, c=values, alpha=0.5, cmap=colors)
	ax.set_ylim(min(a2), max(a2) + 10)
	return im

def graphPerspective(robot, ao, go, ho, fig, axs, xs, ys, zs, values, colors, name):
	'''
    Generate graphs of the workespace's perspectives
    :param robot: manipulator the one to draw
	:param ao: width of the objective region
	:param go: depth of the objective region
	:param ho: height of the objectve region
    :param fig: figure
	:param axs: sobplot lists (one to eachperspective)
	:param xs: list of x coordinates
	:param ys: list of y coordinates
	:param zs: list of z coordinates
	:param values: special points to draw in other colors
	:param colors: colors for the special values
	:param name: name of the subplot
    '''
	im1 = procesGraph(axs[0], xs, zs, values, colors)
	procesGraph(axs[1], ys, zs, values, colors)
	procesGraph(axs[2], xs, ys, values, colors)
	c1 = fig.colorbar(im1, ax=axs[2])
	c1.ax.set_title(name)
	print ho
	print ao
	axs[0].add_patch(Rect(
		(robot.center.x - .5 * ao, robot.center.z - .5 * ho),
		ao, ho, fill=False, color="k", zorder=10., hatch = '/'))
	axs[1].add_patch(Rect(
		(robot.center.y - .5 * go, robot.center.z - .5 * ho),
		go, ho, fill=False, color="k", zorder=10., hatch = '/'))
	axs[2].add_patch(Rect(
		(robot.center.x - .5 * ao, robot.center.y - .5 * go),
		ao, go, fill=False, color="k", zorder=10., hatch = '/'))

def graphXyZ(robot,title, L1, l1, b, pr, ao, go, ho):
	'''
	Generate and save graph of the workspace in 3D
	:param robot: manipulator the one to draw
	:param title: title of the graph
	:param L1: largest linkage of the manipulator
	:param l1: smallest  linkage of the manipulator
    :param b: distane brom center to linkages in the base
    :param pr: distane brom center to linkages in the efector
	:param ao: width of the objective region
	:param go: depth of the objective region
	:param ho: height of the objectve region
	:return:
	'''

	fig, axs = plt.subplots(2,3,figsize=(8, 6))
	fig.canvas.set_window_title(title)
	[[ax.set_aspect('equal', 'box') for ax in a] for a in axs]
	graphPerspective(robot, ao, go, ho, fig, axs[0], xs, ys, zs, ss, 'Greens', "$RI$")
	graphPerspective(robot, ao, go, ho, fig, axs[1], xs, ys, zs, gs, 'Blues', "$CI$")

	title = title.replace(" ", "") + "-pack.png"
	plt.tight_layout()
	fig.suptitle("l =%.2f, L=%.2f, b=%.2f, p=%.2f"%(l1,L1,b,pr))
	fig.savefig(title)

def main():
	global robot, h, a, g, points, res, xs, ys, zs, ss, gs
	ho = input("Altura:")
	ao = input("Anchura:")
	go = input("Profundidad:")

	title = str(raw_input("Nombre (enter para nombre por defecto):") or "N")
	l1 = input("Brazo l1:")
	L1 = input("Brazo L1:")
	b = input("b:")
	pr = input("p:")
	if title == "N":
		title = "DELTA-L%.2f-l%.2f-b%.2f-p%.2f" % (L1, l1, b, pr)
	robot = Delta(l1, L1, b, pr, 10000)

	points = robot.getWorkspace()
	ss = [p.s for p in points]
	gs = [p.ci for p in points]
	points = [(p.x, p.y, p.z) for p in points]
	xs, ys, zs = zip(*points)

	graph3d(robot, title, L1, l1, b, pr, ao, go, ho)
	graphXyZ(robot, title, L1, l1, b, pr, ao, go, ho)


main()