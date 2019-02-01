import time


def apply_rule(rule, a, b, c):
    if rule > 255 or rule < 0:
        raise IOError("Rule value must be between 0 and 255")

    index = 4*a + 2*b + c
    rule_values = str(bin(rule+256))[3::] # Add 256 to ensure string is 8 bits long
    return int(rule_values[7-index])


def next_row(row, rule, wrap=False):
    old_row = row.copy()
    for i in range(len(row)):
        if i == 0:
            if wrap:
                a = old_row[len(row)-1]
            else:
                a = 0
        else:
            a = old_row[i-1]
        b = old_row[i]
        if i == len(row)-1:
            if wrap:
                c = old_row[0]
            else:
                c = 0
        else:
            c = old_row[i+1]
        row[i] = apply_rule(rule, a, b, c)

if __name__ == "__main__":
    row = [0]*80
    row[40] = 1
    rule = 30

    while 1:
        for r in row:
            if r == 1:
                print("*", end = " ")
            else:
                print(" ", end = " ")
        print()
        next_row(row, rule, wrap=True)
        time.sleep(0.1)
