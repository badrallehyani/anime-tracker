
def turn_on():
    if open("isOn", "r").read() == "1":
        return "already running"
    else:
        open("isOn", "w").write("1")
        return "ok"
    
def turn_off():
    if open("isOn", "r").read() == "0":
        return "already off"
    else:
        open("isOn", "w").write("0")
        return "ok"
    
if __name__ == "__main__":
    choice = input("(r)un, (s)top: ")
    if choice == "r":
        print(turn_on())
    elif choice == "s":
        print(turn_off())