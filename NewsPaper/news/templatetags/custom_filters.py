from django import template


register = template.Library()


ban_words = ['сломали', 'сломал', 'болезней', 'захватят']


@register.filter()
def censor(text):
    new_words = []
    for word in text.split():
        if word.isalpha():
            if word.casefold() in ban_words:
                new_words.append('*' * len(word))
            else:
                new_words.append(word)
        else:
            if word.strip("1234567890!@#$%^&*()_+-=[]\"{};':,./<>?").casefold() in ban_words:
                new_chars = []
                for char in word.split():
                    if char.isalpha():
                        new_chars.append('*')
                    else:
                        new_chars.append(char)
                new_words.append(''.join(new_chars))
            else:
                new_words.append(word)
    return ' '.join(new_words)