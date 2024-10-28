from datetime import datetime

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