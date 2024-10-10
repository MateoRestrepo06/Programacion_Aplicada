def comfortable_word(word):
    left_hand = set('qwertasdfgzxcvb')
    right_hand = set('yuiophjklnm')

    current_hand = 'left' if word[0] in left_hand else 'right'

    for letter in word[1:]:
        if current_hand == 'left' and letter in left_hand:
            return False
        elif current_hand == 'right' and letter in right_hand:
            return False

        current_hand = 'left' if letter in left_hand else 'right'

    return True
