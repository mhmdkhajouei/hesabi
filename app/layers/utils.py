import datetime as dt


def text_normalize(text):

    if not isinstance(text, str):
        raise ValueError("text is not a string")

    text = text.strip()

    return text

def par_normalize(par):

    if not isinstance(par, str):
        raise ValueError("par is not a string")

    par = par.strip()

    if par != "":
        par = par.lower()

    return par


def date_formater(date):

    if not isinstance(date, str):
        raise ValueError("date is not a string")

    date = date.strip()

    if date == "":
        raise ValueError("date cannot be empty")

    else:
        try:
            date = dt.datetime.strptime(date, "%Y-%m-%d")

        except:
            raise ValueError("date format is incorrect")

    return date