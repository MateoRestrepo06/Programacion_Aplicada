def frame(arr, border_char):
    max_len = max(len(word) for word in arr)

    border_line = border_char * (max_len + 4)

    framed_strings = [f"{border_char} {word.ljust(max_len)} {border_char}" for word in arr]

    return "\n".join([border_line] + framed_strings + [border_line])
print(frame(['Amo', 'el', 'basket'], '+'))