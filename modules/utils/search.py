def duckduckgo(text):
    return f"https://duckduckgo.com/?q={text}"


def qwant(text):
    return f'https://www.qwant.com/?q={text}'


def discordpy(text):
    return 'https://discordpy.readthedocs.io/en/rewrite/search.html?q={}'.format(text)


def youtube(text):
    return 'https://www.youtube.com/results?search_query={}'.format(text)


def stack(text):
    return 'https://stackoverflow.com/search?q={}'.format(text)
