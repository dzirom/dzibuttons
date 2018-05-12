# dzibuttons
dzi-buttons game is my implementation of the Wrike buttons game I saw on the Codefest 2018 (https://2018.codefest.ru)

Just run this script via Linux console:

$python dzibuttons.py

You can run it on an Android device via QPython interpreter (https://www.qpython.com).

At start of the game you see grid N x N. 'O' means a non-fixed button. 'X' means a fixed button.
Buttons have random-set colors. The goal of the game is to fix the all buttons beginning at an upper left button.
The game does the first step itself. 

The there is a control panel from below. You can choose any color pressing a number color code. 
Once a color has been chosen the adjacent color buttons will be fixed.

![The game screenshot](/images/screenshot1.png)

The challenge goal is to fix buttons faster and for the minimum number of steps.

It's good if you want to make GUI or WebUI for the game. I can remake the module so that this will be more convenient for integration.