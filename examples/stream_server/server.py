
import socket
import multiprocessing
from picamera2.outputs import FfmpegOutput 
    
def listen():
    clients: list[tuple[socket.socket, multiprocessing.Process]] = []
    server.listen(5)
    print("Listening on: ", server.getsockname())
    try:
        while True:
            client, _ = server.accept()
            process = multiprocessing.Process(target=handleClient, args=[client])
            clients.append((client, process))

            process.start()
    except KeyboardInterrupt:
        print("Killing the clients...")
        for [c,p] in clients:
            c.close()
            p.kill()
    

def handleClient(client: socket.socket):
    print("New client: ", client.getpeername())

    file = "video.mp4"
    streamOutput = FfmpegOutput(file)
    streamOutput.start()

    frameSize = pow(2, 15)
    while True:
        frame = client.recv(frameSize)
        if len(frame) == 0: 
            print("Client died")
            streamOutput.stop()
            break

        print(client.getpeername(), "Got a frame: ", len(frame))
        streamOutput.outputframe(frame)

serverAddr = ("", 5001)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(serverAddr)

listen()
server.close()
print("Bye")