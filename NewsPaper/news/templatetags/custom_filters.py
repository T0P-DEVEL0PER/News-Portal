from django import template

register = template.Library()

ban_words = ['сломали', 'сломал', 'болезней', 'захватят']


# forbidden_words = ban_words


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

# @register.filter()
# def hide_forbidden(text):
# new_words = []
# for word in text.split():
# if word.isalpha():
# if word.casefold() in forbidden_words:
# new_words.append(word[0] + '*' * (len(word) - 2) + word[len(word) - 1])
# else:
# new_words.append(word)
# else:
# if word.strip("1234567890!@#$%^&*()_+-=[]\"{};':,./<>?").casefold() in forbidden_words:
# new_chars = []
# new_chars.append(word[0])
# for i in word.strip("1234567890!@#$%^&*()_+-=[]\"{};':,./<>?")[1:len(word) - 1].split():
# new_chars.append('*')
# new_chars.append(word[len(word) - 1])
# new_words.append(''.join(new_chars))
# else:
# new_words.append(word)
# return ' '.join(new_words)
