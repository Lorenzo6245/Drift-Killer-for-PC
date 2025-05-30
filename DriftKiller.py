from inputs import *
from math import pow
from keyboard import press, release, is_pressed
import threading
from customtkinter import CTkButton, CTk, CTkLabel
from pynput.mouse import Controller
from time import sleep

mouse_controller = Controller()

DriftRy = 0.0
DriftRx = 0.0
DriftLx = 0.0
DriftLy = 0.0

Kill = False

class XboxController(object):
    global DriftLx, DriftLy, DriftRx, DriftRy
    MAX_TRIG_VAL = pow(2, 8)
    MAX_JOY_VAL = pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0.0
        self.LeftJoystickX = 0.0
        self.RightJoystickY = 0.0
        self.RightJoystickX = 0.0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target = self._monitor_controller, args = ())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode
        Lx = self.LeftJoystickX
        Ly = self.LeftJoystickY
        Rx = self.RightJoystickX
        Ry = self.RightJoystickY
        #a = self.A
        #b = self.X # b=1, x=2
        #rb = self.RightBumper
        return [Lx, Ly, Rx, Ry]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = (event.state - DriftLy * self.MAX_JOY_VAL) / self.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = (event.state - DriftLx * self.MAX_JOY_VAL) / self.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = (event.state - DriftRy * self.MAX_JOY_VAL) / self.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = (event.state - DriftRx * self.MAX_JOY_VAL) / self.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / self.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / self.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

def moveMouse(dx, dy):
    mouse_controller.move(int(dx), int(dy))

def KillDrift():
    global Kill
    if Kill:
        rx = joy.RightJoystickX
        ry = joy.RightJoystickY
        if abs(rx) > 0.1 or abs(ry) > 0.1:
            moveMouse(rx * 2, -ry * 2)

        if DriftLx != 0:
            if joy.LeftJoystickX != 0:
                if joy.LeftJoystickX > 0.1:
                    release("a")
                    press("d")
                elif joy.LeftJoystickX < 0.1:
                    release("d")
                    press("a")
            elif is_pressed("a") or is_pressed("d"):
                if joy.LeftJoystickX == 0:
                    release("d")
                    release("a")
        if DriftLy != 0:
            if joy.LeftJoystickY != 0:
                if joy.LeftJoystickY > 0.1:
                    release("s")
                    press("w")
                elif joy.LeftJoystickY < 0.1:
                    release("w")
                    press("s")
            elif is_pressed("s") or is_pressed("w"):
                if joy.LeftJoystickY == 0:
                    release("w")
                    release("s")
        
        root.after(1, KillDrift)
            
def Listen():
    global Kill
    if is_pressed("k") and Kill == False:
        Kill = True
        root.after(1, KillDrift)
        Label.configure(text = "Enable", fg_color = "#00ff15")
        sleep(0.5)
    elif is_pressed("k") and Kill == True:
        Kill = False
        Label.configure(text = "Disable", fg_color = "#ff0000")
        sleep(0.5)
    root.after(1, Listen)

def GetData():
    if __name__ == '__main__':
        Lx = int(joy.read()[0] * 100)
        Ly = int(joy.read()[1] * 100)
        Rx = int(joy.read()[2] * 100)
        Ry = int(joy.read()[3] * 100)
        DataLab.configure(text="L Stick: x: " + str(Lx) + "% y: " + str(Ly) + "%" + "\n" + "R Stick x: " + str(Rx) + "% y: " + str(Ry) + "%")
        
        root.after(100, GetData)

def CalculateDrift():
    global DriftLx, DriftLy, DriftRx, DriftRy
    Advice.place(relx = 0.5, rely = 0.7, anchor = "center")
    Advice.configure(text = "KEEP THE CONTROLLER STILL\nPROGRESS: 0%")
    Lx = []
    Ly = []
    Rx = []
    Ry = []
    for i in range(100):
        Lx.append(float(joy.read()[0]))
        Ly.append(float(joy.read()[1]))
        Rx.append(float(joy.read()[2]))
        Ry.append(float(joy.read()[3]))
        Advice.configure(text = f"KEEP THE CONTROLLER STILL\nPROGRESS: {i}%")
    DriftLx = sum(Lx) / 100
    DriftLy = sum(Ly) / 100
    DriftRx = sum(Rx) / 100
    DriftRy = sum(Ry) / 100

    Advice.configure(text = f"Calibration completed!\n Your drift is:\nL Stick: X: {int(DriftLx * 100)}%   Y: {int(DriftLy * 100)}%\nR Stick: X: {int(DriftRx * 100)}%   Y: {int(DriftRy * 100)}%\nPress 'K' to remove the drift")




backgroundcolor = 'black'
root = CTk(className = " Drift Killer")
root.geometry("900x800")
root.configure(background=backgroundcolor)


joy = XboxController()

DataLab = CTkLabel(root, font = ("Roboto", 25), fg_color = "transparent", text_color = "white")
DataLab.place(relx = 0.5, rely = 0.3, anchor = "center")
ButtonMisure = CTkButton(root, text = "Calculate the drift", font = ("Roboto", 25), command = CalculateDrift)
ButtonMisure.place(relx = 0.5, rely = 0.5, anchor = "center")
Advice = CTkLabel(root, font = ("Roboto", 30), text_color = "white", fg_color = "transparent")
Label = CTkLabel(root, text = "Disable", fg_color = "#ff0000", text_color = "black", font = ("Calibri_Light", 25), corner_radius = 2)
Label.place(rely = 0.1, relx = 0.5, anchor = "n")

root.after(1, Listen)
root.after(100, GetData)

root.mainloop()