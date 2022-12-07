from typing import List


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name, path, parent):
        self.name = name
        self.path = path
        self.parent = parent if parent is not None else self
        self.files = []
        self.children = []

    def create_child(self, name):
        child = Directory(name, self.path + "/" + name, self)
        self.children.append(child)
        return child

    def create_file(self, name, size):
        f = File(name, size)
        self.files.append(f)

    def size(self):
        size = 0
        for f in self.files:
            size += f.size
        for d in self.children:
            size += d.size()
        return size


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 95437
        self.test2 = 24933642
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = [line for line in instr.splitlines()]
        self.root = Directory("/", "", None)
        self.all_dirs = [self.root]
        cwd = self.root
        for line in self.data:
            if line.startswith("$ cd"):
                if line == "$ cd ..":
                    cwd = cwd.parent
                elif line == "$ cd /":
                    cwd = self.root
                else:
                    child_dir = line.split(" ")[2]
                    cwd = cwd.create_child(child_dir)
                    self.all_dirs.append(cwd)
            elif not line.startswith("$"):
                if line.startswith("dir"):
                    cwd.create_child(line.split(" ")[1])
                else:
                    size, name = line.split(" ")
                    cwd.create_file(name, int(size))

    def solve(self):
        sizes = []
        for d in self.all_dirs:
            ds = d.size()
            sizes.append(ds)
            if ds < 100000:
                self.part1 += ds

        delete_space = 30000000 - 70000000 + self.root.size()
        sizes.sort()
        for s in sizes:
            if s > delete_space:
                self.part2 = s
                break
