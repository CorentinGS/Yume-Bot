def duckduckgo(text):
    return "https://duckduckgo.com/?q={}".format(text)


def qwant(text):
    return 'https://www.qwant.com/?q={}'.format(text)


def discordpy(text):
    return 'https://discordpy.readthedocs.io/en/rewrite/search.html?q={}'.format(text)


def youtube(text):
    return 'https://www.youtube.com/results?search_query={}'.format(text)


def stack(text):
    return 'https://stackoverflow.com/search?q={}'.format(text)
