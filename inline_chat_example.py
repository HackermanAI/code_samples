

# using python, define a simple made up toy dsl, be creative
# > Here’s a small, made-up toy DSL called “GardenScript”. It’s a tiny language for growing imaginary plants, changing weather, and harvesting “joy”. It’s intentionally simple: each line is one statement.
# > 
# > DSL overview (GardenScript)
# > - PLANT <name> : creates a plant with growth=0 and joy=0
# > - WATER <name> <amount> : increases growth by amount (weather can modify it)
# > - SUN <amount> : increases growth of all plants by amount (weather can modify it)
# > - WEATHER <sunny|rainy|drought> : sets a global modifier
# > - SING <name> "<lyrics>" : increases joy for that plant by number of words in lyrics
# > - HARVEST <name> : prints a harvest report for that plant
# > - SHOW : prints all plants
# > - REPEAT <n> { ... } : repeats the block n times (blocks can nest)
# > 
# > Python implementation (parser + interpreter) and a sample program:

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


# -----------------------------
# AST node definitions
# -----------------------------
@dataclass
class Stmt:
    pass

@dataclass
class PlantStmt(Stmt):
    name: str

@dataclass
class WaterStmt(Stmt):
    name: str
    amount: int

@dataclass
class SunStmt(Stmt):
    amount: int

@dataclass
class WeatherStmt(Stmt):
    mode: str

@dataclass
class SingStmt(Stmt):
    name: str
    lyrics: str

@dataclass
class HarvestStmt(Stmt):
    name: str

@dataclass
class ShowStmt(Stmt):
    pass

@dataclass
class RepeatStmt(Stmt):
    times: int
    body: List[Stmt]


# -----------------------------
# Lexer helpers (line-based DSL)
# -----------------------------
_token_re = re.compile(
    r'''
    "(?:[^"\\]|\\.)*"        |  # quoted string
    \{|\}                   |  # braces
    [A-Za-z_][A-Za-z0-9_]*   |  # identifiers/keywords
    -?\d+                   |  # integers
    [^\s]+                     # fallback tokens
    ''',
    re.VERBOSE
)

def tokenize(program: str) -> List[str]:
    tokens: List[str] = []
    for line in program.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        tokens.extend(_token_re.findall(line))
        tokens.append("\n")  # statement boundary marker
    return tokens


# -----------------------------
# Parser
# -----------------------------
class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[str]):
        self.toks = tokens
        self.i = 0

    def peek(self) -> Optional[str]:
        return self.toks[self.i] if self.i < len(self.toks) else None

    def take(self) -> str:
        if self.i >= len(self.toks):
            raise ParseError("Unexpected end of input")
        t = self.toks[self.i]
        self.i += 1
        return t

    def expect(self, value: str) -> str:
        t = self.take()
        if t != value:
            raise ParseError(f"Expected {value!r}, got {t!r}")
        return t

    def take_eol(self):
        # consume optional extra newlines
        while self.peek() == "\n":
            self.take()

    def parse(self) -> List[Stmt]:
        stmts: List[Stmt] = []
        self.take_eol()
        while self.peek() is not None:
            if self.peek() == "}":
                break
            stmts.append(self.parse_stmt())
            self.take_eol()
        return stmts

    def parse_stmt(self) -> Stmt:
        kw = self.take()
        if kw == "PLANT":
            name = self.take_ident()
            self.consume_to_eol()
            return PlantStmt(name=name)

        if kw == "WATER":
            name = self.take_ident()
            amount = self.take_int()
            self.consume_to_eol()
            return WaterStmt(name=name, amount=amount)

        if kw == "SUN":
            amount = self.take_int()
            self.consume_to_eol()
            return SunStmt(amount=amount)

        if kw == "WEATHER":
            mode = self.take_ident()
            if mode not in ("sunny", "rainy", "drought"):
                raise ParseError("WEATHER must be one of: sunny, rainy, drought")
            self.consume_to_eol()
            return WeatherStmt(mode=mode)

        if kw == "SING":
            name = self.take_ident()
            lyrics = self.take_string()
            self.consume_to_eol()
            return SingStmt(name=name, lyrics=lyrics)

        if kw == "HARVEST":
            name = self.take_ident()
            self.consume_to_eol()
            return HarvestStmt(name=name)

        if kw == "SHOW":
            self.consume_to_eol()
            return ShowStmt()

        if kw == "REPEAT":
            times = self.take_int()
            self.expect("{")
            self.take_eol()
            body = self.parse()
            self.expect("}")
            self.consume_to_eol()
            return RepeatStmt(times=times, body=body)

        raise ParseError(f"Unknown statement keyword: {kw!r}")

    def take_ident(self) -> str:
        t = self.take()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", t):
            raise ParseError(f"Expected identifier, got {t!r}")
        return t

    def take_int(self) -> int:
        t = self.take()
        if not re.fullmatch(r"-?\d+", t):
            raise ParseError(f"Expected integer, got {t!r}")
        return int(t)

    def take_string(self) -> str:
        t = self.take()
        if len(t) >= 2 and t[0] == '"' and t[-1] == '"':
            # unescape basic sequences
            inner = t[1:-1]
            inner = inner.replace(r'\"', '"').replace(r"\\", "\\").replace(r"\n", "\n").replace(r"\t", "\t")
            return inner
        raise ParseError(f"Expected quoted string, got {t!r}")

    def consume_to_eol(self):
        # consume until newline marker or end
        while self.peek() not in (None, "\n"):
            self.take()
        if self.peek() == "\n":
            self.take()


# -----------------------------
# Interpreter
# -----------------------------
class GardenRuntimeError(Exception):
    pass

class Garden:
    def __init__(self):
        self.weather = "sunny"
        self.plants: Dict[str, Dict[str, Any]] = {}

    def ensure(self, name: str):
        if name not in self.plants:
            raise GardenRuntimeError(f"Unknown plant {name!r}. Use PLANT {name} first.")

    def weather_multiplier(self) -> float:
        # This affects WATER and SUN.
        if self.weather == "sunny":
            return 1.0
        if self.weather == "rainy":
            return 1.3
        if self.weather == "drought":
            return 0.4
        return 1.0

    def plant(self, name: str):
        if name in self.plants:
            # idempotent-ish: keep existing but nudge joy
            self.plants[name]["joy"] += 1
            return
        self.plants[name] = {"growth": 0, "joy": 0}

    def water(self, name: str, amount: int):
        self.ensure(name)
        m = self.weather_multiplier()
        gain = int(round(amount * m))
        self.plants[name]["growth"] += max(0, gain)

    def sun(self, amount: int):
        m = self.weather_multiplier()
        gain = int(round(amount * m))
        for p in self.plants.values():
            p["growth"] += max(0, gain)

    def set_weather(self, mode: str):
        self.weather = mode

    def sing(self, name: str, lyrics: str):
        self.ensure(name)
        # joy from word count + a tiny rhyme bonus if last two words match
        words = [w for w in re.findall(r"[A-Za-z']+", lyrics) if w]
        joy = len(words)
        if len(words) >= 2 and words[-1].lower() == words[-2].lower():
            joy += 3
        self.plants[name]["joy"] += joy

    def harvest(self, name: str) -> str:
        self.ensure(name)
        p = self.plants[name]
        # "essence" is a made-up derived stat
        essence = p["growth"] * 2 + p["joy"]
        # harvesting resets growth but keeps joy as "memories"
        report = (
            f"HARVEST {name}: growth={p['growth']} joy={p['joy']} essence={essence} weather={self.weather}"
        )
        p["growth"] = 0
        return report

    def show(self) -> str:
        if not self.plants:
            return "GARDEN: (empty)"
        items = []
        for name in sorted(self.plants.keys()):
            p = self.plants[name]
            items.append(f"{name}(growth={p['growth']}, joy={p['joy']})")
        return f"GARDEN weather={self.weather}: " + ", ".join(items)


def run(program: str) -> List[str]:
    tokens = tokenize(program)
    ast = Parser(tokens).parse()

    g = Garden()
    output: List[str] = []

    def exec_block(stmts: List[Stmt]):
        for s in stmts:
            if isinstance(s, PlantStmt):
                g.plant(s.name)
            elif isinstance(s, WaterStmt):
                g.water(s.name, s.amount)
            elif isinstance(s, SunStmt):
                g.sun(s.amount)
            elif isinstance(s, WeatherStmt):
                g.set_weather(s.mode)
            elif isinstance(s, SingStmt):
                g.sing(s.name, s.lyrics)
            elif isinstance(s, HarvestStmt):
                output.append(g.harvest(s.name))
            elif isinstance(s, ShowStmt):
                output.append(g.show())
            elif isinstance(s, RepeatStmt):
                for _ in range(s.times):
                    exec_block(s.body)
            else:
                raise GardenRuntimeError(f"Unhandled statement: {s}")

    exec_block(ast)
    return output


# -----------------------------
# Example GardenScript program
# -----------------------------
if __name__ == "__main__":
    program = r'''
    # Welcome to GardenScript
    WEATHER rainy
    PLANT MoonFern
    PLANT EmberTulip

    WATER MoonFern 3
    SING MoonFern "silver rivers, silver rivers"
    SUN 2

    REPEAT 3 {
        WATER EmberTulip 2
        SING EmberTulip "bright light"
    }

    SHOW
    HARVEST MoonFern
    HARVEST EmberTulip
    SHOW
    '''

    for line in run(program):
        print(line)
        
# GARDEN weather=rainy: EmberTulip(growth=12, joy=6), MoonFern(growth=7, joy=4)
# HARVEST MoonFern: growth=7 joy=4 essence=18 weather=rainy
# HARVEST EmberTulip: growth=12 joy=6 essence=30 weather=rainy
# GARDEN weather=rainy: EmberTulip(growth=0, joy=6), MoonFern(growth=0, joy=4)

# > If you want, I can tweak the DSL to support variables (like “SET x 3”), conditions (IF joy > 10 { ... }), or a more whimsical syntax (like using punctuation-only spells).

