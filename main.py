import classes.py
import PySimpleGUI as sg

layout = [[]]

def main():
    window = sg.Window('chess', layout)
    while True:
        events, values = window.read()
        if events == sg.WINDOW_CLOSED:
            window.close()
            break
        
        
        print(events, values) # DEBUGS
    return

if __name__ == "__main__":
    main()
