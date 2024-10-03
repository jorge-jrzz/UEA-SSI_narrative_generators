class DualOutput:
    def __init__(self, file, terminal):
        self.file = file
        self.terminal = terminal

    def write(self, message):
        self.file.write(message)
        self.terminal.write(message)

    def flush(self):
        self.file.flush()
        self.terminal.flush()


class DualInput:
    def __init__(self, file, input_func=input):
        self.file = file
        self.input_func = input_func

    def __call__(self, prompt=""):
        response = self.input_func(prompt)
        self.file.write(prompt + response + "\n")
        self.file.flush()
        return response
