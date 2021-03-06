from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Global variables
commonFont = 'fonts/JetBrainsMono'
black = (54, 54, 54)
blue = (52, 73, 94)


def ordinal(n: int) -> str:
    array = ['th', 'st', 'nd', 'rd']
    if (n % 100) > 9 and (n % 100) < 20:
        return str(n) + 'th'
    return str(n) + array[0 if(n % 10) > 3 else n % 10]


def getSeason(_season) -> str:
    return '0' + _season if len(_season) == 1 else _season


def crop(_img, _right):
    _img = _img.crop((0, 0, _right, _img.size[1]))
    return _img


def resize(_img, _compressValue):
    _img = _img.resize(
        (_img.size[0] - _compressValue, _img.size[1]), Image.ANTIALIAS)
    return _img


def endPoint(_name, _fontSize) -> float:
    length = len(_name)
    charSize = _fontSize * 0.4392116714
    spaceSize = charSize * 0.3742203742
    return (length * charSize) + (length * spaceSize)


def genImage(participantName):
    img = Image.new('RGBA', (6000, 350), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    _fontSize = 180
    _font = ImageFont.truetype(commonFont + '-Medium.ttf', _fontSize)
    draw.text((0, 40), participantName, font=_font, fill=black)
    _endpoint = endPoint(participantName, _fontSize)
    compressValue = max(0, _endpoint - 2500 + 380)
    img = crop(img, _endpoint)
    img = resize(img, int(compressValue))
    return img


def addName(_particaipantName):
    front = genImage(_particaipantName)
    back = Image.open('template.jpg')
    front = front.convert('RGBA')
    back = back.convert('RGBA')
    back.paste(front, (380, 940), front)
    return back


def putName(_name) -> None:
    return addName(_name)


def putSignature(_draw, _x, _y, _name, _font) -> None:
    signature = []
    signature.append(ImageFont.truetype('fonts/BrothersideSignature.otf', 90))
    signature.append(ImageFont.truetype('fonts/Theprestigesignature.otf', 90))

    _draw.text((_x, _y), _name, font=signature[_font], anchor='ms', fill=black)


def putInfo(_draw, _x, _y, _name, _designation, _font) -> None:
    _nameFont = ImageFont.truetype(commonFont + '-Medium.ttf', 60)
    _designationFont = ImageFont.truetype(commonFont + '-Thin.ttf', 50)

    _draw.text((_x, _y), _name.upper(),
               font=_nameFont, anchor='ms', fill=black)

    _draw.text((_x, _y + 78), _designation,
               font=_designationFont, anchor='ms', fill=black)

    putSignature(_draw, _x, _y - 135, _name.title(), _font)


class Bootcamp(object):
    season = 0
    participants = 0

    def __init__(self, _season, _participants) -> None:
        self.participants = _participants
        self.season = _season


class Participant(Bootcamp):
    name = ''
    rank = 0
    solve = 0
    uid = ''

    def __init__(self, _name, _rank, _solve, _bootcamp) -> None:
        self.name = _name
        self.rank = _rank
        self.solve = _solve
        super().__init__(_bootcamp.season, _bootcamp.participants)


def genUniqueID(_participant: Participant) -> str:
    # Dummy values
    return _participant.name[0] + str(_participant.season) + str(_participant.solve) + '1234567890ABCDE'


def work(_participant, _instructor, _advisor, _date, ) -> None:
    # Fonts
    font0 = ImageFont.truetype(commonFont + '-Medium.ttf', 180)
    font1 = ImageFont.truetype('fonts/OstrichSans-Bold.ttf', 230)
    font2 = ImageFont.truetype(commonFont + '-Bold.ttf', 60)
    font3 = ImageFont.truetype(commonFont + '-Medium.ttf', 25)

    # Participant name

    img = putName(_participant.name)
    draw = ImageDraw.Draw(img)

    # Season on badge
    draw.text((3005, 1185), 'S' + str(_participant.season),
              font=font1, anchor='mm', fill=blue)

    # Season on text
    draw.text((1595, 1358), str(_participant.season),
              font=font2, anchor='mm', fill=black)

    # Solve percentage
    draw.text((948, 1498), str(_participant.solve) +
              '%', font=font2, anchor='mm', fill=black)

    # Rank
    draw.text((1960, 1498), ordinal(_participant.rank),
              font=font2, anchor='lm', fill=black)

    # Total participants
    draw.text((633, 1568), str(_participant.participants),
              font=font2, anchor='mm', fill=black)

    # Unique ID
    draw.text((2995, 235), _participant.uid,
              font=font3, anchor='lm', fill=black)

    # Issue date
    draw.text((3250, 2309), _date, font=font3, anchor='mm', fill=black)

    # NSUPS information
    putInfo(draw, 1865, 2340, _instructor, 'Season ' +
            getSeason(str(_participant.season)) + ' Instructor', 0)
    putInfo(draw, 790, 2340, _advisor, 'NSUPS Advisor', 1)

    return img


def generate(participantName: str, contestRank: int, solvePercentage: int, bootcampSeason: int, totalParticaipants: int,
             instructorName: str, advisorName: str, uniqueID: str, issueDate: str) -> None:

    bootcamp = Bootcamp(bootcampSeason, totalParticaipants)
    participant = Participant(participantName.upper(),
                              contestRank, solvePercentage, bootcamp)
    participant.uid = uniqueID

    return work(participant, instructorName, advisorName, issueDate)
