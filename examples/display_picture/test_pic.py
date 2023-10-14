'''
The purpose of this file is to show beginners
how to simply display a gif on a tkinter UI.
'''

from tkinter import *

# # create the canvas, size in pixels
# canvas = Canvas(width=300, height=200, bg='black')

# # pack the canvas into a frame/form
# canvas.pack(expand=YES, fill=BOTH)

# # load the .gif image file
# gif1 = PhotoImage(file='avatar2.gif')

# # put gif image on canvas
# # pic's upper left corner (NW) on the canvas is at x=50 y=10
# canvas.create_image(50, 10, image=gif1, anchor=NW)

# # run it ...
# mainloop()


if __name__ == '__main__':
    root = Tk()
    root.geometry('600x300')
    # root.minsize(300, 300)
    root.title('Tic Tac Toe')
    # root.resizable(0, 0)

    # tic tac toe
    gameFrame = Frame(root, width=300, height=300, bg='red')
    gameFrame.grid(rowspan=2, column=0) # rowspan is not 0 based
    canvas = Canvas(gameFrame, height=300, width=300, bd=0)
    canvas.pack(anchor=CENTER)
    canvas.create_line(100, 0, 100, 300, width=5)
    canvas.create_line(200, 0, 200, 300, width=5)
    canvas.create_line(0, 100, 300, 100, width=5)
    canvas.create_line(0, 200, 300, 200, width=5)

    gif1 = PhotoImage(file='avatar2.gif')

    # put gif image on canvas
    # pic's upper left corner (NW) on the canvas is at x=50 y=10
    canvas.create_image(0, 0, image=gif1, anchor=NW)
    # canvas.bind("<Button-1>", player_move)

    root.mainloop()