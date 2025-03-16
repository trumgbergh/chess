from subprocess import PIPE, Popen

stockfish_dest = "stockfish/stockfish/stockfish-ubuntu-x86-64-avx2"


class Communicator:
    def __init__(self):
        self.process = Popen(
            stockfish_dest, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True
        )
        self.write("uci")
        uci_response = self.read()
        while uci_response != "uciok":
            uci_response = self.read()

    def checkready(self):
        self.write("isready")
        response = self.read()
        if response != "readyok":
            return False
        return True

    def write(self, message):
        self.process.stdin.write(f"{message}\n")
        self.process.stdin.flush()

    def read(self):
        return self.process.stdout.readline().strip()

    def settings(self, elo, threads):
        if self.checkready():
            self.write(f"setoption name Threads value {threads}")
            print(f"{self.read()=}")
        if self.checkready():
            self.write("setoption name UCI_LimitStrength value true")
        if self.checkready():
            self.write(f"setoption name UCI_Elo value {elo}")

    def move(self, uci_moves, maxdepth, movetime):
        s = "position startpos moves "
        position = s + "".join(uci_moves)
        self.write(position)
        run = f"go depth {maxdepth} movetime {movetime}"
        self.write(run)
        response = self.read().split(" ")
        while response[0] != "bestmove":
            response = self.read().split(" ")
        return response

    def stop_running(self):
        self.process.communicate(input="quit")
        self.process.stdin.close()
        self.process.terminate()
