import sys
import threading
from models import *
import os

sys.setrecursionlimit(20000)
threading.stack_size(0x2000000)


def clear() -> None:
    os.system('cls')


def parser(command: str, graph: Graph) -> None:
    command = command.split(',')
    command = [i.lower() for i in command]
    command = [int(i) if i.isdigit() else i.replace(" ", "").replace("-", '') for i in command]

    for instruction in command:
        if instruction in ['show']:
            graph.show()
            input("[any]: ")

        elif instruction in ['edges']:
            graph.new_edges()

        elif instruction in ['euler']:
            graph.generate_eulerian()
            input(f"graph is eulerian now [any]: ")

        elif instruction in ["epath"]:
            t = threading.Thread(target=graph.euler_cycle)
            t.start()
            t.join()
            input("[any]: ")

        elif instruction in ["hpath"]:
            t = threading.Thread(target=graph.ham_cycle)
            t.start()
            t.join()
            input("[any]: ")


        elif instruction in ['eulerian']:
            temp = "" if graph.is_eulerian() else " not"
            input(f"Graph is{temp} eulerian. [any]: ")

        elif instruction in ["isolate"]:
            node = graph.isolate_node()
            input(f"isolated node: {node} [any]:")

        elif instruction in ['h', 'help']:
            print("eulerian - check if graph is eulerian")
            print("isolate - isolate one node")
            print("euler - generate eulerian graph and set edges")
            print("show - print graph representations")
            print("epath - find eulerian cycle")
            print("hpath - find all hamiltonian cycles")
            input("[any]: ")

        else:
            input("Command invalid [any]: ")


def main() -> None:
    graph = Graph()
    menu: str = 'default'
    factor = 0


    while True:

        if menu == "default":
            clear()
            input("Graph commander [any]: ")
            menu = 'factor'

        elif menu == "factor":
            fail = False
            while 1:
                clear()
                if fail:
                    print('I don\'t understand. use [n: 1 >= int >= 0]')
                temp = input("Enter graph fullness factor [n: 1 >= int >= 0/exit]: ")
                if temp == 'exit' or (temp.replace(".", "", 1).isdigit() and float(temp) >= 0 and float(temp) < 1):
                    break
                fail = True
            if temp == 'exit':
                break
            factor = float(temp)
            menu = 'choose data'


        elif menu == "choose data":
            fail = False
            while 1:
                clear()
                if fail:
                    print('I don\'t understand. use [enter/gen/exit]')
                temp = input("Enter data or generate [enter/gen/exit]: ").lower()
                if temp in ['gen', 'enter', 'exit']:
                    break
                fail = True
            if temp == 'exit':
                break

            menu = temp

        elif menu == 'gen':
            fail = False
            while 1:
                clear()
                if fail:
                    print('I don\'t understand. use [n: int > 0]')
                temp = input("Enter number of nodes [n: int > 0/exit]: ").lower()
                if temp == 'exit' or (temp.isdigit() and int(temp) > 0):
                    break
                fail = True
            if temp == 'exit':
                break
            n = int(temp)
            graph.init_edges(factor=factor, user=False, n=n)
            menu = 'choose func'

        elif menu == 'enter':
            graph.init_edges(factor=factor, user=True)
            input("[any]: ")
            menu = 'choose func'

        elif menu == "choose func":
            clear()

            command = input("Enter command (h for help) [valid command/h/exit]: ")
            if command == 'exit':
                break
            parser(command, graph)
    clear()


main()
