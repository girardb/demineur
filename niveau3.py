from appJar import gui

def press(button):
    pass

class Button:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'x'

app = gui()

app.addLabel("title", "Minesweeper")
app.setLabelBg("title", "red")
buttons = []
for i in range(9):
    button = Button(i)
    buttons.append(button)
app.addButtons(buttons, press)




if __name__ == '__main__':
    app.go()
