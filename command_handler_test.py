import command_handler
import datetime
import pytz

def test_invalid_command():
    state = {}
    q = "this command doesn't contain anything important for us"
    message, row = command_handler.parse(q, state)
    assert not state
    assert row is None
    assert "Nothing" in message

def test_start_breastfeeding():
    state = {}
    q = "start breastfeeding on the left"
    message, row = command_handler.parse(q, state)

    assert state["side"] == "L"
    assert state["start_query"] == q
    assert state["start"] <= datetime.datetime.now(pytz.UTC)

    assert row is None

def test_stop_breastfeeding():
    state = {
        "side": "R",
        "start_query": "test start query on the right",
        "start" : datetime.datetime.now(pytz.UTC),
    }
    q = "stop breastfeeding"
    message, row = command_handler.parse(q, state)

    assert not state
    assert row is not None
    assert row[1] == "breastfeeding"
    assert row[4] == "R"

def test_diaper():
    state = {}
    q = "went all the way with 40 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "diaper"
    assert row[5] == True and row[6] == True
    assert row[7] == "40"
    assert row[8] == "g"

    q = "went number one with 23 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "diaper"
    assert row[5] == True and row[6] == False
    assert row[7] == "23"
    assert row[8] == "g"

    q = "went number 1 with 23 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "diaper"
    assert row[5] == True and row[6] == False
    assert row[7] == "23"
    assert row[8] == "g"

    q = "went number two with 32 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "diaper"
    assert row[5] == False and row[6] == True
    assert row[7] == "32"
    assert row[8] == "g"

    q = "went number 2 with 32 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "diaper"
    assert row[5] == False and row[6] == True
    assert row[7] == "32"
    assert row[8] == "g"

    q = "had a mixed diaper with 70 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "diaper"
    assert row[5] == True and row[6] == True
    assert row[7] == "70"
    assert row[8] == "g"

    q = "had a mixed diaper"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "diaper"
    assert row[5] == True and row[6] == True
    assert row[7] is None
    assert row[8] is None

    q = "is clean as a flower"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "diaper"
    assert row[5] == False and row[6] == False
    assert row[7] == 0
    assert row[8] == "g"

def test_weight():
    state = {}
    q = "is 3245 grams heavy"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "3245"
    assert row[8] == "g"

    q = "weighs 3600 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "3600"
    assert row[8] == "g"

    q = "mass 3601 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "3601"
    assert row[8] == "g"

    q = "is 3500 grams"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "3500"
    assert row[8] == "g"

    q = "weight"
    message, row = command_handler.parse(q, state)

    assert row is None

def test_length():
    state = {}
    q = "is 50 centimeters long"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "50"
    assert row[8] == "cm"

    q = "length 54 cm"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "54"
    assert row[8] == "cm"

    q = "is 52 cm high"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "52"
    assert row[8] == "cm"

    q = "height is 53 cm"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "53"
    assert row[8] == "cm"

    q = "56 centimeters"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "56"
    assert row[8] == "cm"

    q = "height"
    message, row = command_handler.parse(q, state)

    assert row is None

def test_bath():
    state = {}
    q = "is bathing"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "bath"

    q = "is swimming"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[1] == "bath"

def test_breastpump():
    state = {}
    q = "expressed 50 mililiters from the left side"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[4] == "L"
    assert row[7] == "50"
    assert row[8] == "ml"

    q = "pumped 70 ml"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "70"
    assert row[8] == "ml"

    q = "pumped"
    message, row = command_handler.parse(q, state)

    assert row is None

def test_bottlefeeding():
    state = {}
    q = "took a bottle of 50 mililiters"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "50"
    assert row[8] == "ml"

    q = "drank 70 ml"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[7] == "70"
    assert row[8] == "ml"

    q = "was drinking"
    message, row = command_handler.parse(q, state)

    assert row is None

def test_comment():
    state = {}
    q = "comment ima osip"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[9] == "comment ima osip"

def test_comment():
    state = {}
    q = "medicine kapi"
    message, row = command_handler.parse(q, state)

    assert row is not None
    assert row[9] == " kapi"


