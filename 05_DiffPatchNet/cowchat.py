#!/usr/bin/env python3
import asyncio
import cowsay
import enum

cow_clients = {}
available_cows = cowsay.list_cows()


async def chat(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    login = ""
    read_cmd = asyncio.create_task(reader.readline())
    receive: asyncio.Task | None = None
    while not reader.at_eof():
        print(len([task for task in (read_cmd, receive) if task]))
        done, _ = await asyncio.wait(
            [task for task in (read_cmd, receive) if task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        should_quit = False
        for q in done:
            if q is read_cmd:
                send = read_cmd
                cmd = q.result().decode().strip()
                read_cmd = asyncio.create_task(reader.readline())
                if not cmd:
                    continue
                cmd = cmd.split()
                match cmd[0]:
                    case "who":
                        writer.write(
                            "Cows online:\n{}\n".format("\n".join(cow_clients)).encode()
                        )
                        await writer.drain()
                    case "cows":
                        writer.write(
                            "Cows offline:\n{}\n".format(
                                "\n".join(available_cows)
                            ).encode()
                        )
                        await writer.drain()
                    case "quit":
                        should_quit = True
                        break
                    case "login":
                        if len(cmd) != 2:
                            writer.write("login command usage: login <cow>\n".encode())
                            await writer.drain()
                            continue
                        requested_login = cmd[1]
                        if requested_login not in available_cows:
                            writer.write(
                                f"{requested_login} is not available\n".encode()
                            )
                            await writer.drain()
                            continue
                        available_cows.remove(requested_login)
                        cow_clients[requested_login] = asyncio.Queue()
                        login = requested_login
                        receive = asyncio.create_task(cow_clients[login].get())
                    case "yield":
                        if len(cmd) == 1:
                            writer.write(
                                "yield command usage: yield <message>\n".encode()
                            )
                            await writer.drain()
                            continue
                        if not login:
                            writer.write("You have to login first!\n".encode())
                            await writer.drain()
                            continue
                        for out in cow_clients.values():
                            if out is not cow_clients[login]:
                                text = " ".join(cmd[1:])
                                await out.put(cowsay.cowsay(text, cow=login))
                    case "say":
                        if len(cmd) < 3:
                            writer.write(
                                "say command usage: say <cow> <message>\n".encode()
                            )
                            await writer.drain()
                            continue
                        if not login:
                            writer.write("You have to login first!\n".encode())
                            await writer.drain()
                        cow = cmd[1]
                        if cow in cow_clients.keys():
                            text = " ".join(cmd[2:])
                            await cow_clients[cow].put(cowsay.cowsay(text, cow=login))
                        else:
                            writer.write(f"{cow} is not logged in!\n".encode())
                            await writer.drain()
            elif q is receive:
                receive = asyncio.create_task(cow_clients[login].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
        if should_quit:
            break
    send.cancel()
    if receive:
        receive.cancel()
    if login:
        del cow_clients[login]
        available_cows.append(login)
    print(f"{login} disconnected")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
