import matplotlib.pyplot as plt


def draw_line():
    ax = plt.gca()
    xy = plt.ginput(10)
    x = [p[0] for p in xy]
    y = [p[1] for p in xy]
    line = plt.plot(x, y)
    ax.figure.canvas.draw()
    print(xy)


fig = plt.figure(figsize=(16, 10))
plt.xlim(0, 1600)
plt.ylim(0, 1000)

for _ in range(10):
    draw_line()