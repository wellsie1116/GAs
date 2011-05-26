#!/usr/bin/python2

from life import *

class BoardView(gtk.DrawingArea):
    __gsignals__ = {"expose-event": "override"}

    def __init__(self, width, height):
        gtk.DrawingArea.__init__(self)
        self.width = width
        self.height = height
        self.grid = None
    
    def do_expose_event(self, event):
        g = self.window.cairo_create()
        g.paint()
        g.set_line_width(1.0)
        
        w, h = self.window.get_size()
        stepx = float(w) / self.width
        stepy = float(h) / self.height

        if self.grid:
            for x in range(self.width):
                for y in range(self.height):
                    val = self.grid.getCell(x, y)
                    if val > 0:
                        g.set_source_rgb(0.5, 0.5, 0.5)
                        g.rectangle(x * stepx, y * stepy, stepx, stepy)
                        g.fill_preserve()
                        g.stroke()
                      
        g.set_source_rgb(1.0, 1.0, 1.0)
        g.set_antialias(cairo.ANTIALIAS_NONE)
        
        for x in range(self.width + 1):
            g.move_to((float(x) / self.width) * w, 0)
            g.line_to((float(x) / self.width) * w, h)

        for y in range(self.height + 1):
            g.move_to(0, (float(y) / self.height) * h)
            g.line_to(w, (float(y) / self.height) * h)

        g.stroke()
            

class MainWindow(gtk.Window):
    __gsignals__ = {"expose-event": "override"}

    def __init__(self, rows, cols, width, height):
        gtk.Window.__init__(self)
        self.set_title('Life GA')
        vbox = gtk.VBox()

        self.rows = rows
        self.cols = cols

        self.table = gtk.Table(rows, cols)

        self.views = [[BoardView(width, height) for x in range(cols)] for y in range(rows)]

        for x in range(cols):
            for y in range(rows):
                self.table.attach(self.views[x][y], x, x+1, y, y+1, xpadding=5, ypadding=5)

        vbox.pack_start(self.table, True, True)

        self.add(vbox)
        vbox.show_all()

        self.set_size_request(300, 300)

    def setBoards(self, boards):
        for x in range(self.cols):
            for y in range(self.rows):
                self.views[x][y].grid = boards[y*self.cols + x]
        self.queue_draw()

    def do_expose_event(self, event):
        gtk.Window.do_expose_event(self, event)
        #print "exposed"

    def showStep(self):
        pass



    #def btnStart_clicked(self, event):
    #    self.btnStart.hide()
    #    self.btnStop.show()
    #    self.startdelay = int(self.spnDelayAdj.value)
    #    self.timer = gobject.timeout_add(self.startdelay, self.step)
        
    #def btnStop_clicked(self, event):
    #    self.btnStop.hide()
    #    self.btnStart.show()
    #    gobject.source_remove(self.timer)

    #def step(self):
    #    self.canvas.grid.step()
    #    self.canvas.queue_draw()
    #    if self.startdelay != self.spnDelayAdj.value:
    #        self.startdelay = int(self.spnDelayAdj.value)
    #        self.timer = gobject.timeout_add(self.startdelay, self.step)
    #        return 0
    #    return 1


def main():
    rows = 3
    cols = 3
    count = rows * cols

    width = 10
    height = 10

    gen = Generation(0)
    gen.randomize(count, width, height)

    boards = [Board(genome) for genome in gen.genomes]

    win = MainWindow(rows, cols, width, height)
    win.connect('destroy', gtk.main_quit)
    win.show()

    win.setBoards(boards)

    scores = {}
    def step():
        for board in boards:
            aliveCells = board.step()
            if aliveCells:
                scores[board] = scores.get(board, 0) + 1
        win.queue_draw()
        return 1

    gobject.timeout_add(500, step)

    gtk.main()

if __name__ == '__main__':
    main()

