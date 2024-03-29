import cmd
import shlex
import socket
import sys
import threading
import time
import readline

mut = threading.Lock()


class CowchatClient(cmd.Cmd):
    def __init__(self, sock: socket.socket) -> None:
        super().__init__("tab", None, None)
        self.sock = sock

    def do_login(self, arg):
        """
        Usage: login <cow>
        Login under avialable cow.
        """
        arg = arg.strip()
        args = shlex.split(arg)
        if len(args) != 1:
            print("Usage: login <cow>")
            return
        self.sock.send(f"login {arg}\n".encode())

    def complete_login(self, text, line, begidx, endidx):
        global mut
        args = shlex.split(line[:endidx] + ".")
        if len(args) == 2:
            mut.acquire()
            self.sock.send("cows\n".encode())
            opts = self.sock.recv(1024).decode().strip().split("\n")
            mut.release()
            return [opt for opt in opts[1:] if opt.startswith(text)]
        return []

    def do_say(self, arg):
        """
        Usage: say <cow> <message>
        Send message to cow.
        """
        arg = arg.strip()
        args = shlex.split(arg)
        if len(args) != 2:
            print("Usage: say <cow> <message>")
            return
        self.sock.send(f"say {args[0]} {args[1]}\n".encode())

    def complete_say(self, text, line, begidx, endidx):
        args = shlex.split(line[:endidx] + ".")
        if len(args) == 2:
            mut.acquire()
            self.sock.send("who\n".encode())
            opts = self.sock.recv(1024).decode().strip().split("\n")
            mut.release()
            return [opt for opt in opts[1:] if opt.startswith(text)]
        return []

    def do_cows(self, arg):
        self.sock.send("cows\n".encode())

    def do_who(self, arg):
        self.sock.send("who\n".encode())

    def do_quit(self, arg):
        global is_running
        is_running = False
        mut.acquire()
        self.sock.send("quit\n".encode())
        self.sock.close()
        mut.release()
        exit(0)


def async_recv(cmdline, sock: socket.socket):
    global mut
    while True:
        time.sleep(0.5)
        try:
            mut.acquire()
            sock.setblocking(False)
            msg = sock.recv(1024).decode().strip()
            sock.setblocking(True)
        except BlockingIOError:
            sock.setblocking(True)
            continue
        except OSError:
            break
        finally:
            mut.release()
        if msg:
            print(
                f"{msg}\n{cmdline.prompt}{readline.get_line_buffer()}",
                end="",
                flush=True,
            )


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    s.connect((host, port))
    client = CowchatClient(s)
    client.prompt = "(chat) "
    async_recv_t = threading.Thread(target=async_recv, args=(client, s))
    async_recv_t.start()
    client.cmdloop()
