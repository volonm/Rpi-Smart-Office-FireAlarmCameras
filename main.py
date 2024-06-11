
from src import node

def main():
    print("Starting the application...")
    startNode()

def startNode():
    node.start()

try:
    main()
except KeyboardInterrupt:
    print("The application is closed")

    