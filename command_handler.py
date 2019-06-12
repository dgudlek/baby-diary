import datetime
import pytz


def build_breastfeeding_row(datetime_start, datetime_end, which_side, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "breastfeeding",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                datetime_end.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                which_side,
                None,
                None,
                None,
                None,
                comment,
    ]

def build_diaper_row(datetime_start, pee, poop, quantity, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "diaper",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                None,
                None,
                pee,
                poop,
                quantity,
                "g" if quantity is not None else None,
                comment,
    ]

def build_weight_row(datetime_start, keyword,quantity, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "weight",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                None,
                None,
                None,
                None,
                quantity,
                "g",
                comment,
    ]

def build_length_row(datetime_start, quantity, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "length",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                None,
                None,
                None,
                None,
                quantity,
                "cm",
                comment,
    ]

def build_bath_row(datetime_start, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "bath",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                None,
                None,
                None,
                None,
                None,
                None,
                comment,
    ]

def build_breastpump_row(datetime_start, which_side, quantity, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "breastpump",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                None,
                which_side,
                None,
                None,
                quantity,
                "ml",
                comment,
    ]

def build_bottlefeeding_row(datetime_start, quantity, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "bottlefeeding",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                None,
                None,
                None,
                None,
                quantity,
                "ml",
                comment,
    ]

def build_comment_row(datetime_start, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "comment",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                None,
                None,
                None,
                None,
                None,
                None,
                comment,
    ]

def build_medicine_row(datetime_start, comment):
    return [
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%d/%m/%Y"),
                "medicine",
                datetime_start.astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                None,
                None,
                None,
                None,
                None,
                None,
                comment,
    ]

def extract_quantity(q):
    quantity = None
    for qty in q.split(" "):
        if qty.isdigit():
            if qty != 1 and qty != 2:
                quantity = qty
    return quantity

# returns (bool, row)
def try_parse_diaper(q):
    if q:
        is_pee = 0
        is_poop = 0
        pee_keywords = ["pee", "number one", "number 1"]
        for pee_kw in pee_keywords:
            if pee_kw in q:
                is_pee = 1
        poop_keywords = ["poo", "number two", "number 2"]
        for poop_kw in poop_keywords:
            if poop_kw in q:
                is_poop = 1

        if "went all the way" in q:
            is_pee = 1
            is_poop = 1

        if "mixed" in q:
            is_pee = 1
            is_poop = 1

        if "clean" in q:
            row = build_diaper_row(
                        datetime.datetime.now(pytz.UTC),
                        0,
                        0,
                        0,
                        q)
            return (True, row)

        if is_pee or is_poop:
            quantity = extract_quantity(q)
            row = build_diaper_row(
                        datetime.datetime.now(pytz.UTC),
                        is_pee,
                        is_poop,
                        quantity,
                        q)
            return (True, row)

    return (False, None)



# returns (bool, row)
def try_parse_weight(q):
    if q:
        qty = extract_quantity(q)
        if qty is None:
            return (False, None)

        keywords = ["weight", "weighs", "heavy", "mass", "gram"]
        for kw in keywords:
            if kw in q:
                row = build_weight_row(
                            datetime.datetime.now(pytz.UTC),
                            "weight",
                            qty,
                            q)
                return (True, row)
    return (False, None)

# returns (bool, row)
def try_parse_length(q):
    if q:
        qty = extract_quantity(q)
        if qty is None:
            return (False, None)

        keywords = ["long", "length", "high", "height", "centimeters"]
        for kw in keywords:
            if kw in q:
                row = build_length_row(
                            datetime.datetime.now(pytz.UTC),
                            qty,
                            q)
                return (True, row)
    return (False, None)

# returns (bool, row)
def try_parse_bath(q):
    if q:
        keywords = ["bath", "swimm"]
        for kw in keywords:
            if kw in q:
                row = build_bath_row(
                            datetime.datetime.now(pytz.UTC),
                            q)
                return (True, row)

    return (False, None)

# returns (bool, row)
def try_parse_breastpump(q):
    if q:
        qty = extract_quantity(q)
        if qty is None:
            return (False, None)

        keywords = ["pump", "express"]
        for kw in keywords:
            if kw in q:
                sides = ["left", "right"]
                which_side = None
                for side in sides:
                    if side in q:
                        if side == "left":
                            which_side = "L"
                        elif side == "right":
                            which_side = "R"

                row = build_breastpump_row(
                            datetime.datetime.now(pytz.UTC),
                            which_side,
                            qty,
                            q)
                return (True, row)
    return (False, None)

# returns (bool, row)
def try_parse_bottlefeeding(q):
    if q:
        qty = extract_quantity(q)
        if qty is None:
            return (False, None)

        keywords = ["bottle", "drink", "drank"]
        for kw in keywords:
            if kw in q:
                row = build_bottlefeeding_row(
                            datetime.datetime.now(pytz.UTC),
                            qty,
                            q)
                return (True, row)
    return (False, None)

# returns (bool, row)
def try_parse_comment(q):
    if q:
        if "comment" in q:
            row = build_comment_row(datetime.datetime.now(pytz.UTC), q)
            return (True, row)
    return (False, None)

# returns (bool, row)
def try_parse_medicine(q):
    if q:
        keywords = ["medicine", "med"]
        for kw in keywords:
            if kw in q:
                row = build_medicine_row(datetime.datetime.now(pytz.UTC), q.replace(kw, ""))
                return (True, row)
    return (False, None)


# IN: q, state
# OUT: (message, row)
def parse(q, state):
    if q and "start" in q:
        state["start"] = datetime.datetime.now(pytz.UTC)
        state["start_query"] = q
        if "right" in q:
            state["side"] = "R"
        elif "left" in q:
            state["side"] = "L"
        else:
            return ("Side not recognized.", None)
        print ("Start, state persisted: ", state)
        return ("Started.", None)

    elif q and "stop" in q:
        if "start" not in state:
            print ("Stop, but state not initialized: ", state)
            return ("Stop, not initialized.", None)
        else:
            comment = "%s; %s" % (state["start_query"], q)
            print ("Stop, logged, previous state: ", state, "; state reset.")
            row = build_breastfeeding_row(
                        state["start"],
                        datetime.datetime.now(pytz.UTC),
                        state["side"],
                        comment)
            del state["start"]
            del state["start_query"]
            del state["side"]
            return ("Logged.", row)

    elif q:
        is_diaper, diaper_row = try_parse_diaper(q)
        if is_diaper:
            return ("Checked diaper.", diaper_row)

        is_weight, weight_row = try_parse_weight(q)
        if is_weight:
            return ("Weight checked.", weight_row)

        is_length, length_row = try_parse_length(q)
        if is_length:
            return ("Length checked.", length_row)

        is_bath, bath_row = try_parse_bath(q)
        if is_bath:
            return ("Bathing checked.", bath_row)

        is_breastpump, breastpump_row = try_parse_breastpump(q)
        if is_breastpump:
            return ("Breastpump checked.", breastpump_row)

        is_bottlefeeding, bottlefeeding_row = try_parse_bottlefeeding(q)
        if is_bottlefeeding:
            return ("Bottlefeeding checked.", bottlefeeding_row)

        is_comment, comment_row = try_parse_comment(q)
        if is_comment:
            return ("Comment.", comment_row)

        is_medicine, medicine_row = try_parse_medicine(q)
        if is_medicine:
            return ("Medicine.", medicine_row)

    return ("Nothing happend", None)



