import os
import signal
import readline
from datetime import datetime, date


def convertStr(ls):
    s = ""
    for i in ls:
        s += i
    return s


def parse(inp):
    arg = []
    args = []
    i = 0
    while i < len(inp):
        # print("inp", inp[i])
        if inp[i] != chr(92) and inp[i] != ' ' and inp[i] != '"':
            arg.append(inp[i])
            i = i + 1

        elif inp[i] == '"':
            # arg.append(inp[i])
            i += 1
            while i < len(inp) - 1 and inp[i] != '"':
                arg.append(inp[i])
                i = i + 1
            i += 1
            args.append(convertStr(arg))
            arg = []
            i = i + 1

        elif inp[i] == ' ':

            if inp[i - 1] == chr(92):

                arg.append(' ')

            else:
                args.append(convertStr(arg))
                arg = []
            i = i + 1
        else:
            i = i + 1
    if convertStr(arg) != '':
        args.append(convertStr(arg))

    file = args[0]

    return file, args


def cd(path):
    return os.chdir(path)


def pwd():
    return os.getcwd()


def getColor():
    filename = "config.txt"

    with open(filename) as f:
        content = f.readlines()

    bgline = content[0]
    fgline = content[1]

    bg = bgline.split(":")[1]
    fg = fgline.split(":")[1]

    return int(bg), int(fg)


def changColor():
    num1, num2 = getColor()

    print("\x1b[" + str(num1) + ";" + str(num2) + "m")


changColor()

if __name__ == '__main__':
    bgList = []
    bgId = []
    today = date.today()
    print("Today's date:", today)
    while True:
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')

        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        command = input(str(t) + " shimshell>> ")

        if len(command) == 0:
            continue
        file, args = parse(command)
        flag = 0
        if command == 'exit':
            exit(0)
        elif command == "bglist":
            if len(bgList) < 1:
                print("no bg job")
            for i in range(len(bgList)):
                print("( " + str(i + 1) + " )" + convertStr(bgList[i]))

        elif args[0] == "bgkill":
            if int(args[1]) - 1 < 0:
                print("invalid process number ")
            else:
                os.kill(bgId[int(args[1]) - 1], signal.SIGTERM)
                del bgList[int(args[1]) - 1]
                del bgId[int(args[1]) - 1]

        elif args[0] == "bgstop":
            if int(args[1]) - 1 < 0:
                print("invalid process number ")
            else:
                os.kill(bgId[int(args[1]) - 1], signal.SIGSTOP)

        elif args[0] == "bgstart":
            if int(args[1]) - 1 < 0:
                print("invalid process number ")
            else:
                os.kill(bgId[int(args[1]) - 1], signal.SIGCONT)

        else:

            if args[0] == 'bg':
                flag = 1
                file = args[1]
                args = args[1:]
                bgList.append(' '.join(str(a) for a in args))

            if command is None:
                print("Error")
                os.exite(1)
            if file == 'cd':
                cd(convertStr(args[1:]))

                continue
            if file == 'pwd':
                print(pwd())
                continue

            p_id = os.fork()
            if flag == 1:
                bgId.append(int(p_id))

            if p_id == 0:
                a = os.execvp(file, args)
                if a < 0:
                    print("eoror", file)
                    os.exit(1)
            elif p_id < 0:
                print("Fork failed")
                exit(1)
            else:
                if flag == 0:
                    status = 0
                    os.waitpid(p_id, status)
                else:
                    os.waitpid(p_id, os.WNOHANG)
