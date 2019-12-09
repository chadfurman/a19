my_range = 172930-683082
lower_bound = 177777
upper_bound = 679999
digits = [1,7,7,7,7,7]
valid_password_count = 0

def is_valid_password(first, second, third, fourth, fifth, sixth):
    password = (first * 100000) + (second * 10000) + (third * 1000) + (fourth * 100) + (fifth * 10) + sixth
    numlist = [first,second,third,fourth,fifth,sixth]
    doubles_pass = False
    if first == second and second != third:
        doubles_pass = True
    if second == third and third != fourth and second != first:
        doubles_pass = True
    if third == fourth and fourth != fifth and third != second:
        doubles_pass = True
    if fourth == fifth and fifth != sixth and fourth != third:
        doubles_pass = True
    if fifth == sixth and fifth != fourth:
        doubles_pass = True
                
    if not doubles_pass:
        return False
    if first > second or second > third or third > fourth or fourth > fifth or fifth > sixth:
        return False
    if lower_bound > password or password > upper_bound:
        return False
    print(password)
    return True


def main():
    valid_password_count = 0
    for first_digit in range(1,10):
        if first_digit > 6:
            break;
        for second_digit in range(first_digit,10):
            if second_digit < first_digit:
                continue
            for third_digit in range(second_digit,10):
                if third_digit < second_digit:
                    continue
                for fourth_digit in range(third_digit,10):
                    if fourth_digit < third_digit:
                        continue
                    for fifth_digit in range(fourth_digit,10):
                        if fifth_digit < fourth_digit:
                            continue
                        for sixth_digit in range(fifth_digit,10):
                            if sixth_digit < fifth_digit:
                                continue
                            if (is_valid_password(first_digit, second_digit, third_digit, fourth_digit, fifth_digit, sixth_digit)):
                                valid_password_count += 1
    return valid_password_count

if __name__ == "__main__":
    print(str(main()))
