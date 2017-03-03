def decode(text):
    pass


def encode(text):
    if text:
        meow = chr(21941)
        uc0 = chr(8251)  # 0  ※  8251   203b
        uc1 = chr(9651)  # 1  △  9651   25b3
        uc2 = chr(9671)  # 2  ◇  9671   25c7
        uc3 = chr(9675)  # 3  ○  9675   25cb
        uc4 = chr(9678)  # 4  ◎  9678   25ce
        uc5 = chr(9679)  # 5  ●  9679   25cf
        uc6 = chr(9734)  # 6  ☆  9734   2606
        uc7 = chr(9733)  # 7  ★  9733   2605
        uc8 = chr(12290)  # 8  。  12290  3002
        uc9 = chr(21596)  # 9  呜  21596  545c
        uc10 = chr(21714)  # 10 哒  21714  54d2
        uc11 = chr(21780)  # 11 唔  21780  5514
        uc12 = chr(26114)  # 12 昂  26114  6602
        uc13 = chr(65281)  # 13 ！  65281  ff01
        uc14 = chr(65311)  # 14 ？  65311  ff1f
        uc15 = chr(65374)  # 15 ～  65374  ff5e

        list = []
        list.append(uc0)
        list.append(uc1)
        list.append(uc2)
        list.append(uc3)
        list.append(uc4)
        list.append(uc5)
        list.append(uc6)
        list.append(uc7)
        list.append(uc8)
        list.append(uc9)
        list.append(uc10)
        list.append(uc11)
        list.append(uc12)
        list.append(uc13)
        list.append(uc14)
        list.append(uc15)

        res = meow
        for word in text:
            append_res = ""
            ucs = (hex(ord(word)) + "")[2:]
            for uc in ucs:
                index = ord(uc)
                if index >= 48 and index <= 48 + 10 - 1:
                    append_res += list[index - 48]
                    pass
                elif index >= 97 and index <= 97 + 6 - 1:
                    append_res += list[index - 97 + 10]
                    pass
                else:
                    print("error")
            res += append_res + meow
        return res
    else:
        return "encode error"


if __name__ == "__main__":
    text = "lalala"

    print(encode(text))

    print(str)