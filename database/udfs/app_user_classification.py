def classify_generation(birthyear):
    if 1997 <= birthyear:
        return 'Gen Z'
    elif 1981 <= birthyear <= 1996:
        return 'Millennial'
    elif 1965 <= birthyear <= 1980:
        return 'Gen X'
    elif 1946 <= birthyear <= 1964:
        return 'Baby Boomer'
    else:
        return 'Other'