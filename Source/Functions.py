from dublib.Methods.Filesystem import ReadJSON

from datetime import datetime

import re

def DeleteSymbols(zodiak):

    Symbols = [
        "♈",
        "♉", 
        "♊",
        "♋",
        "♌",
        "♍",
        "♎",
        "♏",
        "♐",
        "♑",
        "♒",
        "♓"
        ]
            
    
    for symbol in Symbols:
        if symbol in zodiak:
            new_zodiak = zodiak.replace(symbol + " ", "")

            return new_zodiak

def GetTodayDate() -> str:
    return datetime.today().date().strftime("%d.%m.%Y")

def MirrorText(Text: str, First_Zodiak: str, Second_Zodiak: str) -> str:
    match = re.search(r"💞 (.*?) & (.*?) 💞", Text)
    if match:
        sign1 = match.group(1)
        sign2 = match.group(2)
        new_str = f"💞 {sign2} & {sign1} 💞"
        New_Text = Text.replace(f"💞 {Second_Zodiak} & {First_Zodiak} 💞", new_str)

    return New_Text

def ChangeMorphology(Text: str, First_Zodiak: str, Second_Zodiak: str):
    Positions_First = list()
    Positions_Second = list()
    Zodiak_Cases = ReadJSON("Zodiacs.json")
    for Case in Zodiak_Cases.values():
        Positions_First.append(Case[First_Zodiak])
        Positions_Second.append(Case[Second_Zodiak])
    start_index_First = find_second_occurrence_index(Text)
    Text, Replaced_First = replace_earliest(Text, Positions_First, "First", start_index = start_index_First)
    start_index_Second = find_second_occurrence_index(Text)
    Text, Replaced_Second  = replace_earliest(Text, Positions_Second, "Second", start_index = start_index_Second)
    Text = Text.replace("First", Replaced_Second).replace("Second", Replaced_First)

    return Text 

def replace_earliest(text: str, values: list, flag: str, start_index):

    if not isinstance(text, str):
        raise TypeError("Текст должен быть строкой.")
    if not isinstance(values, list):
        raise TypeError("Значения должны быть списком.")

    earliest_first_occurrence_index = float('inf')
    value_to_replace = None
    
    for value in values:
        pattern = r"\b" + re.escape(str(value)) + r"\b"
        match = re.search(pattern, text[start_index:])
        if match:
            first_match_index = match.start() + start_index
            if first_match_index < earliest_first_occurrence_index:
                earliest_first_occurrence_index = first_match_index
                value_to_replace = value
                


    if value_to_replace is not None:
        pattern = r"\b" + re.escape(str(value_to_replace)) + r"\b"
        match = re.search(pattern, text[start_index:])
        if match and match.start() + start_index == earliest_first_occurrence_index:
            replacement_start_index = match.start() + start_index
            text = text[:replacement_start_index] + flag + text[replacement_start_index + len(str(value_to_replace)):]
            return text, value_to_replace
    else:
        return text, None

def find_second_occurrence_index(text, pattern="💞"):
    matches = list(re.finditer(pattern, text))
    if len(matches) >= 2:
        return matches[1].start()
    else:
        return None