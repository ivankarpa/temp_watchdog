import time


class Subprocess:
    def run_subprocess(self):
        while True:
            f = open('../subprocess/file.txt', 'w')
            f.write("a")
            f.close()
            time.sleep(1)


if __name__ == '__main__':
    Subprocess().run_subprocess()
