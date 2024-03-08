import cmd
import cowsay
import shlex


class CowsayCmd(cmd.Cmd):
    prompt = "(say to cow) "

    def do_list_cows(self, arg):
        """
        Usage: list_cows.
        Print available cows.
        """
        args = shlex.split(arg)
        if len(args) > 0:
            print("Usage: list_cows [directory]")
            return
        print(", ".join(cowsay.list_cows()))

    def do_make_bubble(self, arg):
        """
        Usage: make_bubble text [brackets]
        Print bubble with your thoughts specified in text parameter.
        Avaiable options for brackets: cowsay, cowthink.
        """
        args = shlex.split(arg)
        if len(args) == 0 or len(args) > 2:
            print("Usage: make_bubble text [brackets]")
            return
        if len(args) == 2:
            args[-1] = cowsay.THOUGHT_OPTIONS[args[-1]]
        print(cowsay.make_bubble(*args))

    def complete_make_bubble(self, text, line, begidx, endidx):
        args = shlex.split(line[:endidx] + ".")
        if len(args) == 3:
            return [opt for opt in ["cowsay", "cowthink"] if opt.startswith(text)]
        return []

    def do_cowsay(self, arg):
        """
        Usage: cowsay message [cow [eyes [tongue]]]
        Print cowsay message with the default cow, eyes and tongue if tey are not specified.
        cow, eyes and tongue parameters are optional.
        """
        args = shlex.split(arg)
        if len(args) == 0 or len(args) > 4:
            print("Usage: cowsay message [cow [eyes [tongue]]]")
            return
        match len(args):
            case 1:
                print(cowsay.cowsay(args[0]))
            case 2:
                print(cowsay.cowsay(args[0], cow=args[1]))
            case 3:
                print(cowsay.cowsay(args[0], cow=args[1], eyes=args[2]))
            case 4:
                print(cowsay.cowsay(args[0], cow=args[1], eyes=args[2], tongue=args[3]))

    def complete_cowsay(self, text, line, begidx, endidx):
        args = shlex.split(line[:endidx] + ".")
        if len(args) == 3:
            return [opt for opt in cowsay.list_cows() if opt.startswith(text)]
        return []

    def do_cowthink(self, arg):
        """
        Usage: cowthink message [cow [eyes [tongue]]]
        Print cowthink message with the default cow, eyes and tongue if tey are not specified.
        cow, eyes and tongue parameters are optional.
        """
        args = shlex.split(arg)
        if len(args) == 0 or len(args) > 4:
            print("Usage: cowthink message [cow [eyes [tongue]]]")
            return
        match len(args):
            case 1:
                print(cowsay.cowthink(args[0]))
            case 2:
                print(cowsay.cowthink(args[0], cow=args[1]))
            case 3:
                print(cowsay.cowthink(args[0], cow=args[1], eyes=args[2]))
            case 4:
                print(cowsay.cowthink(args[0], cow=args[1], eyes=args[2], tongue=args[3]))

    def complete_cowthink(self, text, line, begidx, endidx):
        args = shlex.split(line[:endidx] + ".")
        if len(args) == 3:
            return [opt for opt in cowsay.list_cows() if opt.startswith(text)]
        return []



if __name__ == "__main__":
    print(cowsay.cowsay("Let's talk to some cows!", cow="frogs"))
    CowsayCmd().cmdloop()
