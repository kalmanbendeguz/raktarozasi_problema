class Warehouse:
    def __init__(self):
        self.dimsOfWarehouse = [0, 0]
        self.numOfPillars = 0
        self.numOfPallets = 0
        self.posOfPillars = []
        self.dimsOfPallets = []


class Pallet:
    def __init__(self, _index):
        self.size = [0, 0]  # height, width when horizontal
        self.index = _index


class Position:
    def __init__(self):
        self.coordinates = [-1, -1]
        self.vertical = True


class Hozzarendeles:
    pallet = Pallet(0)
    position = Position()

    def __init__(self, _lerakando: Pallet, _position: Position):
        self.pallet = _lerakando
        self.position = _position


class Node:
    h = Hozzarendeles

    def __init__(self, _h: Hozzarendeles):
        self.h = _h


class Oszlop:
    def __init__(self, y, x):
        self.position = [y, x]


wh = Warehouse()
hozzarendelesek = []  # hozzarendeles[]
matrix = []  # int[][]
hozzarendeletlenek = []  # pallet[]
root = Node
numofcalls = 0
numofnumofcalls = 1


def add_to_matrix(hr: Hozzarendeles):
    if hr.position.vertical:
        for i in range(hr.position.coordinates[0], hr.position.coordinates[0] + hr.pallet.size[0]):  # fentről le
            for j in range(hr.position.coordinates[1], hr.position.coordinates[1] + hr.pallet.size[1]):  # balról jobbra
                matrix[i][j] = 1
    if not hr.position.vertical:
        for i in range(hr.position.coordinates[0], hr.position.coordinates[0] + hr.pallet.size[1]):  # fentről le
            for j in range(hr.position.coordinates[1], hr.position.coordinates[1] + hr.pallet.size[0]):  # balról jobbra
                matrix[i][j] = 1


def remove_from_matrix(hr: Hozzarendeles):
    if hr.position.vertical:
        for i in range(hr.position.coordinates[0], hr.position.coordinates[0] + hr.pallet.size[0]):  # fentről le
            for j in range(hr.position.coordinates[1], hr.position.coordinates[1] + hr.pallet.size[1]):  # balról jobbra
                matrix[i][j] = 0
    if not hr.position.vertical:
        for i in range(hr.position.coordinates[0], hr.position.coordinates[0] + hr.pallet.size[1]):  # fentről le
            for j in range(hr.position.coordinates[1], hr.position.coordinates[1] + hr.pallet.size[0]):  # balról jobbra
                matrix[i][j] = 0


def area(p: Pallet):
    return p.size[0] * p.size[1]


def kerulet(p: Pallet):
    return 2*(p.size[0] + p.size[1])


def area_kerulet(p: Pallet):
    return (p.size[0] * p.size[1])*(2*(p.size[0] + p.size[1]))


def init_hozzarendeletlenek():
    for i in range(0, wh.numOfPallets):
        p = Pallet(i + 1)
        p.size = [wh.dimsOfPallets[i][0], wh.dimsOfPallets[i][1]]
        hozzarendeletlenek.append(p)


def init_matrix(_matrix : [], height: int, width: int):
    for i in range(0, height):
        matrix.append([])
        for j in range(0, width):
            matrix[i].append(0)


def print_matrix(_matrix: []):
    for i in range(0, len(_matrix)):
        for j in range(0, len(_matrix[0])):
            if j == len(matrix[i]) - 1:
                print(_matrix[i][j], end="")
                print()
            else:
                print(_matrix[i][j], end="\t")


def hozzarendelesek_teljes(hk: []):
    if len(hk) == wh.numOfPallets:
        return True
    return False


def tavolsag(p: Position):
    return (p.coordinates[0]*p.coordinates[0] + p.coordinates[1] * p.coordinates[1])**(1/2)


def osszkerulet(_p: Position, _lerakando: Pallet):
    hr = Hozzarendeles(_lerakando, _p)
    add_to_matrix(hr)
    keruletke = 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if matrix[i][j] == 0:
                if i != 0:
                    if matrix[i-1][j] == 1:
                        keruletke += 1
                if i != len(matrix) - 1:
                    if matrix[i+1][j] == 1:
                        keruletke += 1
                if j != 0:
                    if matrix[i][j-1] == 1:
                        keruletke += 1
                if j != len(matrix[0]) - 1:
                    if matrix[i][j+1] == 1:
                        keruletke += 1
    remove_from_matrix(hr)
    return keruletke


def tartomany_ertekek_sorrendezese(lerakando: Pallet):
    ertekek = []  # Position[]
    for i in range(0, len(matrix) - lerakando.size[0] + 1):  # csak minden értéket hozzáadunk, hogy odafér-e azzal nem foglalkozunk
        for j in range(0, len(matrix[0]) - lerakando.size[1] + 1):
            pv = Position()
            pv.coordinates = [i, j]
            pv.vertical = True
            if pallet_fits(lerakando, pv):
                ertekek.append(pv)
    for i in range(0, len(matrix) - lerakando.size[1] + 1):  # csak minden értéket hozzáadunk, hogy odafér-e azzal nem foglalkozunk
        for j in range(0, len(matrix[0]) - lerakando.size[0] + 1):
            ph = Position()
            ph.coordinates = [i, j]
            ph.vertical = False
            if pallet_fits(lerakando, ph):
                ertekek.append(ph)
    #print(len(ertekek))
    ertekek.sort(key=lambda x: osszkerulet(x, lerakando), reverse=False)
    for i in range(0, int(len(ertekek) * (9/10))):
        if len(ertekek) > 1:
            ertekek.pop()
    #for i in ertekek:
        #print(osszkerulet(i, lerakando), end="\t")
    return ertekek


def hozzarendeletlen_valtozo_kivalasztasa(node: Node):
    hozzarendeletlenek.sort(key=area_kerulet, reverse=True)
    # hozzarendeletlenek.sort(key=kerulet, reverse=True)
    # hozzarendeletlenek.sort(key=area, reverse=True)
    return hozzarendeletlenek[0]  # vagy size-1


def oszlop_elfer(lerakando: Pallet, position: Position, oszlop: Oszlop):
    if position.vertical:
        if position.coordinates[0] < oszlop.position[0] < position.coordinates[0] + lerakando.size[0]:
            if position.coordinates[1] < oszlop.position[1] < position.coordinates[1] + lerakando.size[1]:
                return False
    if not position.vertical:
        if position.coordinates[0] < oszlop.position[0] < position.coordinates[0] + lerakando.size[1]:
            if position.coordinates[1] < oszlop.position[1] < position.coordinates[1] + lerakando.size[0]:
                return False
    return True


def pallet_fits(lerakando: Pallet, position: Position):
    for i in range(0, wh.numOfPillars):
        o = Oszlop(wh.posOfPillars[i][0], wh.posOfPillars[i][1])
        if not oszlop_elfer(lerakando, position, o):
            return False
    if position.vertical:
        for i in range(position.coordinates[0], position.coordinates[0] + lerakando.size[0]):  # fentről le
            for j in range(position.coordinates[1], position.coordinates[1] + lerakando.size[1]):  # balról jobbra
                if matrix[i][j] != 0:
                    return False
    if not position.vertical:
        for i in range(position.coordinates[0], position.coordinates[0] + lerakando.size[1]):  # fentről le
            for j in range(position.coordinates[1], position.coordinates[1] + lerakando.size[0]):  # balról jobbra
                if matrix[i][j] != 0:
                    return False
    return True


def rekurziv_visszalepeses(local_hozzarendelesek: [], node: Node):  #  local_hozzarendelesek = Hozzarendelesek[]
    global numofcalls
    numofcalls += 1
    #print(numofcalls)
    #if numofcalls > (wh.numOfPallets + wh.numOfPillars) * 2 * numofnumofcalls:
     #   numofcalls = 0
      #  numofnumofcalls += 1
       # lengthnumber = len(hozzarendelesek)
        #for i in range(0, int(lengthnumber/2)):
         #   hozzarendeletlenek.append(hozzarendelesek.pop().pallet)
          #global reversevalues
           # reversevalues = not reversevalues
    if hozzarendelesek_teljes(local_hozzarendelesek):
        return local_hozzarendelesek
    lerakando = hozzarendeletlen_valtozo_kivalasztasa(node)  #  a hozzárendeletlenek globálisan lesznek, az a függvény majd eléri
    for position in tartomany_ertekek_sorrendezese(lerakando):
        #if pallet_fits(lerakando, position): # nem kell, mert már ellenőriztük
        hr = Hozzarendeles(lerakando, position)
        local_hozzarendelesek.append(hr)
        hozzarendeletlenek.remove(lerakando)
        add_to_matrix(hr)
        #print_matrix(matrix)
        childnode = Node(hr)
        eredmeny = rekurziv_visszalepeses(local_hozzarendelesek, childnode)
        if eredmeny is not None:
            return eredmeny
        hozzarendelesek.remove(hr)
        hozzarendeletlenek.append(lerakando)
        remove_from_matrix(hr)
        #print_matrix(matrix)
    return None


def visszalepeses_kereses(_root: Node):
    return rekurziv_visszalepeses(hozzarendelesek, _root)


def read(_wh: Warehouse):
    line_num = 0
    try:
        while True:
            line_num += 1
            line = input()
            split = line.split()
            if line_num == 1:
                _wh.dimsOfWarehouse = [int(split[0]), int(split[1])]
            elif line_num == 2:
                _wh.numOfPillars = int(split[0])
            elif line_num == 3:
                _wh.numOfPallets = int(split[0])
            elif line_num < _wh.numOfPillars + 4:
                _wh.posOfPillars.append([int(split[0]), int(split[1])])
            elif line_num < _wh.numOfPallets + _wh.numOfPillars + 4:
                _wh.dimsOfPallets.append([int(split[0]), int(split[1])])
                if line_num == _wh.numOfPallets + _wh.numOfPillars + 3:
                    break
            else:
                break
    except EOFError:
        pass


# def build_tree(root: Node, depth: int, max_depth: int, b: int):
#     print(depth)
#     if depth == max_depth:
#         root.following_nodes = None
#         return
#     for i in range(0, 3):
#         child = Node()


read(wh)
init_matrix(matrix, wh.dimsOfWarehouse[0], wh.dimsOfWarehouse[1])
init_hozzarendeletlenek()
megoldas: [] = visszalepeses_kereses(root)
if megoldas is None:
    print("nincs megoldas")
    exit(0)
for i in range(0, len(megoldas)):
    if megoldas[i].position.vertical:
        for j in range(megoldas[i].position.coordinates[0], megoldas[i].position.coordinates[0] + megoldas[i].pallet.size[0]):  # fentről le
            for k in range(megoldas[i].position.coordinates[1], megoldas[i].position.coordinates[1] + megoldas[i].pallet.size[1]):  # balról jobbra
                matrix[j][k] = megoldas[i].pallet.index
    if not megoldas[i].position.vertical:
        for j in range(megoldas[i].position.coordinates[0], megoldas[i].position.coordinates[0] + megoldas[i].pallet.size[1]):  # fentről le
            for k in range(megoldas[i].position.coordinates[1], megoldas[i].position.coordinates[1] + megoldas[i].pallet.size[0]):  # balról jobbra
                matrix[j][k] = megoldas[i].pallet.index
print_matrix(matrix)
