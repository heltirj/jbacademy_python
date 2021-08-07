import random


def filter_string(symbols_string):
    new_symbols = ""
    for s in symbols_string:
        if s == "1" or s == "0":
            new_symbols += s
    return new_symbols


def triad_stats(symbols_string):
    stats = {key: {"0": 0, "1": 0} for key in
             ["{0:b}".format(i).zfill(3) for i in range(8)]}
    for i in range(3, len(symbols_string)):
        stats[symbols_string[i - 3:i]][symbols_string[i]] += 1
    return stats


def first_triad(symbols_string):
    stats = {key: 0 for key in
             ["{0:b}".format(i).zfill(3) for i in range(8)]}
    sym_count = len(symbols_string)
    for i in range(0, sym_count - 2):
        stats[symbols_string[i:i + 3]] += 1
    max_k = {"000"}
    max_v = stats["000"]
    for k, v in stats.items():
        if v > max_v:
            max_k = {k}
        elif v == max_v:
            max_k.add(k)
    return random.choice(list(max_k))


def predict(learn_string, input_string):
    stats = triad_stats(learn_string)
    predict_string = first_triad(learn_string)
    count = len(input_string)
    for i in range(count - 3):
        triad = input_string[i:i + 3]
        predict_string += "1" if stats[triad]["1"] > stats[triad]["0"] else "0"
    right_count = sum(
        [int(input_string[i] == predict_string[i]) for i in range(3, count)])
    count = count - 3
    acc = round(right_count / count * 100, 2)
    return {"prediction": predict_string,
            "count": count,
            "right_count": right_count,
            "accuracy": acc}


def check_str(symbols_string):
    for i in symbols_string:
        if i != "0" and i != "1":
            return False
    return True


if __name__ == "__main__":
    symbols = ""
    max_len = 100
    while True:
        print("Print a random string containing 0 or 1:")
        symbols += filter_string(input())
        if len(symbols) < max_len:
            print(f"Current data length is {len(symbols)}, {max_len - len(symbols)} "
                  f"symbols left")
        else:
            print("Final data string:", symbols, sep="\n")
            break
    print()
    capital = 1000
    print('You have $1000. Every time the system successfully predicts your next press, you lose $1.\n'
          'Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!')
    while True:
        i_string = input("Print a random string containing 0 or 1:\n")
        if i_string == "enough":
            break
        if not check_str(i_string):
            continue
        prediction = predict(symbols, i_string)
        print(f"prediction:\n{prediction['prediction']}\n")
        all_count = prediction['count']
        right = prediction['right_count']
        wrong = all_count - right
        accuracy = prediction['accuracy']
        capital = capital - right + wrong
        print(f"Computer guessed right {right} out of {all_count} symbols ({accuracy} %)")
        print(f"Your capital is now ${capital}\n")
        symbols += i_string
    print("Game over!")
