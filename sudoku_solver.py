from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'height', 500)
Config.set('graphics', 'width', 450)


class NumBox(TextInput):
    def __init__(self, **kwargs):
        super(NumBox, self).__init__(**kwargs)
        self.size_hint = (0.111111111, 0.1)
        self.multiline = False
        self.font_size = 30
        self.padding=[16, 8]
        self.bind(focus=self.on_focus)
    def on_focus(self, instance, value):
        if not value:
            if self.text!='' and self.text!='1' and self.text!='2' and self.text!='3' and self.text!='4' and self.text!='5' and self.text!='6' and self.text!='7' and self.text!='8' and self.text!='9':
                self.text=''


class GameBoard(RelativeLayout):
    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.boxlist = []
        for i in range(9):
            boxcol = []
            for j in range(9):
                boxcol.append(NumBox(pos_hint={'x': 0.111111111*i, 'top': 1-0.1*j}))
                self.add_widget(boxcol[j])
            self.boxlist.append(boxcol)
        self.add_widget(Button(text='[b][size=40][font=fonts/ScriptsoftRegular][color=00ff00]SOLVE[/color][/font][/size][/b]', markup=True, background_color=(1,1,1,0.8), size_hint=(0.5, 0.1), pos_hint={'x': 0., 'top': 0.1}, on_press=self.solve))
        self.add_widget(Button(text='[b][size=40][font=fonts/ScriptsoftRegular][color=ff0000]RESET[/color][/font][/size][/b]', markup=True, background_color=(1,1,1,0.8), size_hint=(0.5, 0.1), pos_hint={'x': 0.5, 'top': 0.1}, on_press=self.reset))

    def solve(self, button):
        self.grid=[]
        for i in range(9):
            helper=[]
            for j in range(9):
                if self.boxlist[i][j].text:
                    helper.append(int(self.boxlist[i][j].text))
                else:
                    helper.append(0)
            self.grid.append(helper)
        del helper
        if self.grid==[[0 for x in range(9)] for y in range(9)]:
            self.grid=[[0,0,0,3,0,0,2,0,0],
                       [0,0,0,0,0,8,0,0,0],
                       [0,7,8,0,6,0,1,5,0],
                       [0,4,2,5,1,0,0,0,0],
                       [1,0,6,0,0,0,4,0,9],
                       [0,0,0,0,8,6,1,5,0],
                       [0,3,5,0,9,0,7,6,0],
                       [0,0,0,7,0,0,0,0,0],
                       [0,0,9,0,0,5,0,0,0]]
        GameBoard.solver(self.grid, self.boxlist)
        del self.grid

    def isfull(grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j]==0:
                    return False
        return True

    def possible_entries(grid, i, j):
        possibility_array={}
        for x in range(1,10):
            possibility_array[x]=0
        for y in range(9):
            if not grid[i][y]==0:
                possibility_array[grid[i][y]]=1
        for x in range(9):
            if grid[x][j]!=0:
                possibility_array[grid[x][j]]=1
        if i in (0,1,2):
            h=0
        elif i in (3,4,5):
            h=3
        else:
            h=6
        if j in (0,1,2):
            k=0
        elif j in (3,4,5):
            k=3
        else:
            k=6
        for x in range(h,h+3):
            for y in range(k,k+3):
                if grid[x][y]!=0:
                    possibility_array[grid[x][y]]=1
        for x in range(1,10):
            if possibility_array[x]==0:
                possibility_array[x]=x
            else:
                possibility_array[x]=0
        return possibility_array

    def solver(grid, boxlist):
        possibilities={}
        if GameBoard.isfull(grid):
            for i in range(9):
                for j in range(9):
                    boxlist[i][j].text=str(grid[i][j])
            return
        else:
            for x in range(9):
                for y in range(9):
                    if grid[x][y]==0:
                        i=x
                        j=y
                        break
        possibilities=GameBoard.possible_entries(grid, i, j)
        for x in range(1,10):
            if possibilities[x]!=0:
                grid[i][j]=possibilities[x]
                GameBoard.solver(grid, boxlist)
        grid[i][j]=0

    def reset(self, button):
        for i in self.boxlist:
            for j in i:
                j.text = ''

class SudokuSolver(App):
    def build(self):
        self.gb = GameBoard()
        return self.gb

if __name__=='__main__':
    SudokuSolver().run()
