from random import randint, choice, random


def checkint(query: str, *, mininput: int = 1, maxinput: float = float('inf')) -> int:
    """Check if user input is positive integer, repeat input function if otherwise"""
    while True:
        try:
            ans = int(input(query).strip())
            if mininput <= ans <= maxinput:  # positive, does not accept 0
                return ans
            else:
                raise ValueError
        except ValueError:
            maxno = maxinput
            if maxinput == float('inf'):
                maxno = 'Infinity'
            print(f"Invalid entry. Please enter a number from {mininput}-{maxno}")


def reconst(cls: type, attributes: dict):
    args = []
    for i in range(cls.__init__.__code__.co_argcount - 1):
        args.append(None)
    rebuilt = object.__new__(cls, *args)
    rebuilt.__dict__.update(attributes)
    return rebuilt


class Meta(type):
    def __repr__(cls):
        retstr = ''
        for attr, value in cls.__dict__.items():
            if not callable(value) and attr[:2] != '__':
                retstr += f"{cls.__name__}.{attr} = {value}\n"
        return retstr


class Unit(metaclass=Meta):
    maxhp: int
    value: int

    def __init__(self, lane: int, column: int):
        """Initialise hp and location"""
        self.hp = self.maxhp
        self.lane = lane
        self.column = column
        lanes[self.lane][self.column] = self  # Appear on field

    def __repr__(self):
        return f"reconst({self.__class__.__name__}, {self.__dict__})"

    def __str__(self):
        return f'{laneletters[self.lane]}{self.column + 1} {self.__class__.__name__}'

    def exist(self) -> bool:
        return lanes[self.lane][self.column] is self

    def damaged(self, damage: int = 0) -> bool:
        """Check if unit is killed; if killed return True and remove dead body; else return False"""
        self.hp -= damage
        if self.hp <= 0:  # killed
            self.dead()
            return True
        return False  # Still alive

    def dead(self):
        """process death"""
        if self.exist():
            lanes[self.lane][self.column] = None  # remove dead body
        print(self, "dies!")  # declaration


class Monster(Unit):
    damage: list[int, int]
    speed: int

    def __init__(self):
        """Spawn Monster"""
        while True:  # Generate possible locations until
            randlane = randint(0, settings['lanes'] - 1)
            if lanes[randlane][settings['columns'] - 1] is None:  # Location is empty
                break
            elif isinstance(lanes[randlane][settings['columns'] - 1], Defender):  # Spawning monster smashes Defenders at location
                if isinstance(lanes[randlane][settings['columns'] - 1], Mine):
                    lanes[randlane][settings['columns'] - 1].explode()
                break
        super().__init__(randlane, settings['columns'] - 1)  # Created
        stats['monsterpop'] += 1  # Update Monster population records
        print(f"{self.__class__.__name__} spawns at {laneletters[self.lane]}{self.column + 1}!")

    def move(self, distance: int, phrase: str = 'moves', polite: bool = True):
        """distance: Negative distances move left, positive right
        polite: will monster push other monsters"""
        if distance < 0:
            step = -1
        else:
            step = 1
        lane = lanes[self.lane][self.column + step::step]
        moving = [self]

        def stepping():     # multiple
            lanes[self.lane][self.column] = None  # Monster leaves original square
            for monster in moving:
                if monster.column + step < 0:
                    print(f"A {monster.__class__.__name__} has reached the city! All is lost!\n"
                          "You have lost the game. :(")
                    exit(0)
                elif monster.column + step >= len(lanes[0]):
                    print(monster, 'is pushed off the field!')
                    monster.dead()
                else:
                    monster.column += step
                    print(f"{monster.__class__.__name__} {phrase} to {laneletters[monster.lane]}{monster.column + 1}!")
                    lanes[monster.lane][monster.column] = monster  # Monster reaches next square

        displacement = 0
        for square in lane:
            if isinstance(square, Monster):
                if polite:
                    print(self, 'is blocked from advancing.')
                    return
                else:
                    moving.append(square)
                    continue
            elif isinstance(square, Defender):
                if isinstance(square, Mine):
                    print(moving[-1].__class__.__name__, "triggers Mine!")
                    square.explode()
                    moving = [monster for monster in moving if monster.exist()]
                else:
                    moving[-1].attack()
                    return
            stepping()
            displacement += step
            if displacement == distance:
                return
        while displacement < distance:
            displacement += step
            stepping()

    def attack(self):
        """Monster attack"""
        damage = randint(*self.damage)  # Randomise damage
        print(f"{self} attacks {lanes[self.lane][self.column - 1]}; inflicts {damage} damage!")
        lanes[self.lane][self.column - 1].damaged(damage)  # Injure Defender

    def dead(self):
        """process death"""
        super().dead()
        stats['monsterpop'] -= 1  # Monster population reduced
        stats['killcount'] += 1  # Kill count increase
        stats['gold'] += self.value  # Collect bounty
        print(f"You gain {self.value} gold as a reward.")  # Declare
        stats['threat'] += self.value  # Threat bar increase by Monster’s value.

    @classmethod
    def strengthen(cls):  # Called/12 turns
        cls.damage[0] += 1  # increase min & max damage
        cls.damage[1] += 1
        cls.maxhp += 1  # increase hit points
        cls.value += 1  # increase reward


class Werewolf(Monster):
    maxhp = 10
    value = 3
    damage = [1, 4]
    speed = 2


class Zombie(Monster):
    maxhp = 15
    value = 2
    damage = [3, 6]
    speed = 1


class Defender(Unit):
    def __init__(self, upgradecost: int):
        """Initialise hp, location, upgrade costs, collect payment for unit, and declare entry to playing field"""
        while True:
            lane, column = positionvalidation("Place where? ")
            if lanes[lane][column] is None:  # unoccupied
                super().__init__(lane, column)  # init hp and location
                self.upgradeCost = upgradecost  # init upgrade cost
                stats['gold'] -= self.value  # payment for unit collected
                print(f"\n{self.__class__.__name__} placed at {laneletters[self.lane]}{column + 1}")
                return
            else:  # occupied
                print("Position occupied by", lanes[lane][column].__class__.__name__)

    def upgrade(self) -> bool:
        """Returns True if Defender is upgraded; False if otherwise"""
        print("Upgrading", self, "costs", self.upgradeCost, "gold")  # Show price
        if self.upgradeCost > stats['gold']:  # If not enough gold
            print("You do not have enough gold!")  # Declare
            return False  # Fail to upgrade
        else:  # If enough gold
            while True:  # Repeat until valid input given
                yn = input("Upgrade? (y/n): ").strip().lower()  # Ask to upgrade
                if yn == "y":  # If yes
                    stats['gold'] -= self.upgradeCost  # Collect payment
                    self.upgradeCost += 3  # Upgrade cost increase per upgrade
                    print(self, 'is upgraded\n')
                    return True  # Successfully upgraded
                elif yn == "n":  # If no
                    return False  # Fail to upgrade
                else:  # If invalid input
                    print("Invalid Input! Please enter y or n")  # error message

    def heal(self):
        print(self, f"{self.hp}/{self.maxhp}", sep="\t")  # Current health
        print("Healing costs 2 hp/gold")  # Show price
        while True:  # Repeat until valid input
            payment = checkint("How much are you paying? ", mininput=0,
                               maxinput=(self.maxhp - self.hp) // 2)  # input hp amt with validation
            if payment == 0:  # did not buy heal
                return False  # healing fail
            else:  # if buy heal
                if payment > stats['gold']:  # if Not enough gold
                    print("Not enough gold!")  # Declare
                else:  # if Enough gold
                    self.hp += payment * 2  # healing
                    stats['gold'] -= payment  # collect payment
                    print(self, f'recovers {payment * 2} hp!')  # Declare
                    return True  # healing successful


class Wall(Defender):
    maxhp = 20
    value = 3
    upgradeHeal = 5

    def __init__(self):
        super().__init__(upgradecost=6)  # specify upgrade cost

    def upgrade(self) -> bool:
        if super(Wall, self).upgrade():
            self.hp += self.upgradeHeal  # Increase hit points
            self.maxhp += self.upgradeHeal  # Increase Max hit points
            return True
        else:
            return False


class Archer(Defender):
    maxhp = 5
    value = 5

    def __init__(self):
        super().__init__(upgradecost=8)  # specify upgrade cost
        self.damage = [1, 4]

    def upgrade(self) -> bool:
        if super().upgrade():
            self.hp += 1  # Increase hit points
            self.maxhp += 1  # Increase Max hit points
            self.damage[0] += 1
            self.damage[1] += 1
            return True
        else:
            return False


class Cannon(Defender):
    maxhp = 8
    value = 7
    upamt = 1
    upprob = 0.1
    cooldown = 3

    def __init__(self):
        super().__init__(upgradecost=10)  # specify upgrade cost
        self.damage = [7, 10]
        self.push = 0.4
        self.setup = self.cooldown

    def upgrade(self) -> bool:
        if super().upgrade():
            self.hp += self.upamt  # Increase hit points
            self.maxhp += self.upamt  # Increase Max hit points
            self.damage[0] += self.upamt
            self.damage[1] += self.upamt
            self.push += self.upprob
            if self.cooldown > 1:
                self.cooldown -= 1
            print(self.stat())
            return True
        else:
            return False

    def stat(self):
        return f"HP: {self.hp}/{self.maxhp}\n" \
               f"Damage: {self.damage[0]}-{self.damage[1]}\n" \
               f"Push Probability: {int(self.push * 100)}%\n" \
               f"Firing Rate: {self.setup}/{self.cooldown}"

    def fire(self):
        self.setup += 1
        if self.cooldown <= self.setup:
            if self.push >= random():
                push = True
            else:
                push = False
            self.setup = 0  # fires regardless of monsters
            speed = randint(*self.damage)
            print(f'{self} fires cannon ball at {speed} speed!')
            return speed, push


class Mine(Defender):
    maxhp = None
    value = 8

    def __init__(self):
        super().__init__(upgradecost=2)  # specify upgrade cost
        self.damage = 10

    def upgrade(self) -> bool:
        if super().upgrade():
            self.damage += 2
            return True
        else:
            return False

    def explode(self):
        print('Mine explodes and deals', self.damage, 'damage to nearby monsters!')
        if self.column == 0:
            mincol = 0
        else:
            mincol = self.column - 1
        if self.column == settings['columns']:
            maxcol = settings['columns']
        else:
            maxcol = self.column + 2
        if self.lane == 0:
            minlane = 0
        else:
            minlane = self.lane - 1
        if self.lane == settings['lanes']:
            maxlane = settings['lanes']
        else:
            maxlane = self.lane + 2
        for lane in lanes[minlane:maxlane]:
            for square in lane[mincol:maxcol]:
                if isinstance(square, Monster):
                    square.damaged(self.damage)
        lanes[self.lane][self.column] = None


def setup() -> list[list[None]]:
    battlefield = []
    for lanei in range(settings['lanes']):
        lane = []
        for col in range(settings['columns']):
            lane.append(None)
        battlefield.append(lane)
    return battlefield


stats = {'turn': 0,  # Current Turn
         'killcount': 0,  # Number of monsters killed
         'monsterpop': 0,  # Number of monsters in the field
         'gold': 9,  # Beginning game adds one gold automatically so put init gold 1 less than actual
         'threat': -1,  # Threat metre; start of game adds 1 to begin at 0
         'danger': 1}  # Danger level != 0 cause randint increase threat and monsters strengthen
settings = {'lanes': 4,
            'columns': 8,
            'killcount': 30,
            'threat': 5}
lanes = setup()


def changesettings() -> list[list[None]]:
    while True:
        editsettings = menu(f"Board dimensions:\t{settings['columns']}x{settings['lanes']}",
                            f"Kills needed to win:\t{settings['killcount']}",
                            f"Threat Metre length:\t{settings['threat']}",
                            f"Starting Gold:\t\t{stats['gold'] + 1}",
                            header="Settings:", query="Change: ")
        if editsettings == 1:
            settings['columns'] = checkint("No. of columns: ", mininput=2, maxinput=10)
            settings['lanes'] = checkint("No. of lanes: ", maxinput=26)
        elif editsettings == 2:
            settings['killcount'] = checkint("Kills needed to win: ", maxinput=10 ** 31)
        elif editsettings == 3:
            settings['threat'] = checkint("Threat Metre length: ", maxinput=40)
        elif editsettings == 4:
            stats['gold'] = checkint("Starting Gold: ", mininput=float('-inf')) - 1
        else:
            return setup()


def battle():
    """Defenders and Monsters fight"""
    for lane in lanes:
        arrow = 0
        shelling = []
        for square in lane:
            if isinstance(square, Archer):  # Fire arrow
                arrow += randint(*square.damage)
            if isinstance(square, Cannon):
                tba = square.fire()
                if tba is not None:
                    shelling.append(list(tba))
            if isinstance(square, Monster):
                print()
                if arrow:  # Hit
                    print(f'Arrows rain down on {square}; inflicts {arrow} damage!')
                    square.damaged(arrow)  # dead
                    arrow = 0
                    if not square.exist():
                        continue
                if shelling:
                    for shell in shelling[:]:
                        if shell[0] > square.hp:
                            shell[0] -= square.hp
                            print(f'Cannon ball tears straight through {square}')
                            square.dead()
                            break
                        else:
                            print(f'Cannon ball hits {square} and loses momentum, dealing {shell[0]} damage')
                            if not square.damaged(shell[0]) and shell[1]:
                                square.move(1, 'is pushed back', False)
                            shelling.remove(shell)
                        if not square.exist():
                            break
                if square.exist():
                    square.move(square.speed * -1, 'advances')


def battlefieldisplay(squarespacing: int = 8):
    print(" " * (3 + squarespacing // 2), end="")  # spacing at front
    for columno in range(1, settings['columns'] + 1):  # column numbering
        print(str(columno).ljust(squarespacing + 1), end="")
    print()  # end line
    lanei = 0
    for lane in lanes:  # each lane
        print("  " + "+".ljust(squarespacing + 1, "-") * settings['columns'] + "+")  # lane borders
        # Name row
        print(laneletters[lanei], "|", end="")  # lane lettering + starting vertical line
        for square in lane:  # each square
            if square is None:  # unit name display
                name = ""
            else:
                name = square.__class__.__name__[:squarespacing]  # to fit in box
            print(name.center(squarespacing), end="|")  # print unit name + |
        print()
        # hp row
        print("  ", end="|")  # spacing at front
        for square in lane:  # each square
            if square is None:
                hpstr = ""
            elif square.hp is None:
                hpstr = str(square.damage)
            else:
                hpstr = f"{square.hp}/{square.maxhp}"  # hp display
            print(hpstr.center(squarespacing), end="|")  # print hp + |
        print()  # end line
        lanei += 1
    print("  " + "+".ljust(squarespacing + 1, "-") * settings['columns'] + "+")  # close bottom lane


def menu(*options: str, header: str = "", goback: str = "Exit", query: str = "Your Choice? ") -> int:
    """Menu display with user input validation"""
    print(header)
    i = 1
    for option in options:
        if i % 2 == 1:
            end = "\t"
        else:
            end = "\n"
        print(f"{i}. {option}".ljust(28), end=end)
        i += 1
    print(f"{0}. {goback}")
    return checkint(query, mininput=0, maxinput=i - 1)


def positionvalidation(query: str) -> (str, int):
    while True:
        location = input(query).replace(" ", "").upper()
        if len(location) >= 2:
            if location[0] in laneletters and location[1:].isnumeric():
                column = int(location[1:]) - 1
                if 0 <= column < settings['columns']:
                    return laneletters.index(location[0]), column
        print("Invalid Input! Please enter a lane letter and a column number")


def unitshopping() -> bool:
    unit = menu(*[f"{pickme.__name__} ({pickme.value} gold)" for pickme in Defender.__subclasses__()],
                goback="Don't buy",
                header="What unit do you wish to buy? ")
    if unit == 0:
        return False
    Picked = Defender.__subclasses__()[unit - 1]
    if Picked.value <= stats['gold']:
        Picked()
        return True
    print("Not enough gold")
    return False


def unitupgrade() -> bool:
    while True:
        lane, column = positionvalidation("Enter position of unit: ")
        if isinstance(lanes[lane][column], Defender):
            return lanes[lane][column].upgrade()
        else:
            print("Not a defensive unit")
            return False


def heal() -> bool:
    while True:
        lane, column = positionvalidation("Enter position of unit: ")
        if isinstance(lanes[lane][column], Defender) and not isinstance(lanes[lane][column], Mine):
            if lanes[lane][column].heal():
                return True
            else:
                return False
        else:
            print(lanes[lane][column], "cannot be healed")


def turning():
    """Turn processing."""
    stats['turn'] += 1  # Time Advances
    stats['threat'] += randint(1, stats['danger'])  # threat amount increased by rand no. 1 - danger level
    stats['gold'] += 1  # reward survival
    print()
    spawncount = 0
    while stats['threat'] >= settings['threat'] and spawncount != settings['lanes']:  # if threat metre filled up
        choice(Monster.__subclasses__())()  # 1 monster spawned/metre length overflow
        stats['threat'] -= settings['threat']
        spawncount += 1
    if stats['monsterpop'] == 0:  # if empty field spawn monster
        choice(Monster.__subclasses__())()
    if stats['turn'] % 10 == 0:  # /10 turns
        stats['danger'] += 1  # danger level increases
        for Attacker in Monster.__subclasses__():  # Each Monster type strengthens
            Attacker.strengthen()
        print("Evil Strengthens!")


def savegame():
    with open("stats.txt", "w") as savefile:
        savefile.write(f"stats = {stats}\n"
                       f"settings = {settings}\n"
                       f"lanes = {lanes}\n")  # saved stats and settings to stats.txt
        for Monstertype in Monster.__subclasses__():
            savefile.write(repr(Monstertype))
    print("\nGame saved!")


def loadgame():
    with open("stats.txt", "r") as savefile:
        exec(savefile.read(), globals())  # To affect global namespace to assign global variables
    print("\nGame loading...")


# Main Program
initchoice = menu("Start new game", "Load saved game", "Settings",
                  header="Desperate Defenders\n"
                         "-------------------\n"
                         "Defend the city from undead monsters!")
if initchoice == 3:  # Settings
    lanes = changesettings()  # have to init lanes before this for board dimensions
    initchoice = 1  # Begin New game
if initchoice == 2:  # load game
    loadgame()
if initchoice == 1 or 2:  # Play game
    laneletters = tuple(map(chr, range(65, 91)))[:settings['lanes']]  # lane alphabets
    while stats['killcount'] < settings['killcount']:  # loop until Reach killcount
        if initchoice == 2:  # load game
            initchoice = 1
        elif initchoice == 1:
            turning()
        while True:
            battlefieldisplay()
            chosen = menu("Buy unit", "Upgrade unit", "Heal unit", "End Turn", "Save game",
                          header=f"Turn {stats['turn']}\t\t\t"
                                 f"Threat: [{('-' * stats['threat']).ljust(settings['threat'])}]\t\t\t"
                                 f"Danger Level: {stats['danger']}\n"
                                 f"Gold: {stats['gold']}\t\t\t"
                                 f"Kill Count: {stats['killcount']}/{settings['killcount']}")
            if chosen == 1:  # Buy Unit
                if unitshopping():
                    break
            elif chosen == 2:
                if unitupgrade():
                    break
            elif chosen == 3:
                if heal():
                    break
            elif chosen == 4:  # end turn
                break
            elif chosen == 5:
                savegame()
            elif chosen == 0:  # Quit Game
                print("\nSee you next time!")
                exit(0)
        battle()
print("You have protected the city! You win!")  # declare Victory!
