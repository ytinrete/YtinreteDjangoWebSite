
var meow = String.fromCharCode(21941)
var uc0 = String.fromCharCode(8251)//0  ※  8251   203b
var uc1 = String.fromCharCode(9651)//1  △  9651   25b3
var uc2 = String.fromCharCode(9671)//2  ◇  9671   25c7
var uc3 = String.fromCharCode(9675)//3  ○  9675   25cb
var uc4 = String.fromCharCode(9678)//4  ◎  9678   25ce
var uc5 = String.fromCharCode(9679)//5  ●  9679   25cf
var uc6 = String.fromCharCode(9734)//6  ☆  9734   2606
var uc7 = String.fromCharCode(9733)//7  ★  9733   2605
var uc8 = String.fromCharCode(12290)//8  。  12290  3002
var uc9 = String.fromCharCode(21596)//9  呜  21596  545c
var uc10 = String.fromCharCode(21714)//10 哒  21714  54d2
var uc11 = String.fromCharCode(21780)//11 唔  21780  5514
var uc12 = String.fromCharCode(26114)//12 昂  26114  6602
var uc13 = String.fromCharCode(65281)//13 ！  65281  ff01
var uc14 = String.fromCharCode(65311)//14 ？  65311  ff1f
var uc15 = String.fromCharCode(65374)//15 ～  65374  ff5e

function kittyEncode(text){
    var res = meow
    for (var i = 0; i < text.length; i++) {
        var uni16 = text.charCodeAt(i).toString(16)
        var appendRes = ""
        for (var j=0; j<uni16.length; j++){
            switch(uni16.charCodeAt(j)){
               case 48:
                   appendRes = appendRes + uc0
                   break
               case 49:
                   appendRes = appendRes + uc1
                   break
               case 50:
                   appendRes = appendRes + uc2
                   break
               case 51:
                   appendRes = appendRes + uc3
                   break
               case 52:
                   appendRes = appendRes + uc4
                   break
               case 53:
                   appendRes = appendRes + uc5
                   break
               case 54:
                   appendRes = appendRes + uc6
                   break
               case 55:
                   appendRes = appendRes + uc7
                   break
               case 56:
                   appendRes = appendRes + uc8
                   break
               case 57:
                   appendRes = appendRes + uc9
                   break
               case 97:
                   appendRes = appendRes + uc10
                   break
               case 98:
                   appendRes = appendRes + uc11
                   break
               case 99:
                   appendRes = appendRes + uc12
                   break
               case 100:
                   appendRes = appendRes + uc13
                   break
               case 101:
                   appendRes = appendRes + uc14
                   break
               case 102:
                   appendRes = appendRes + uc15
                   break
               default:
                   break
               }
        }
        if (appendRes!=""){
            res = res + appendRes + meow
        }
    }
    return res
}
function kittyDecode(text){
    var res = ""
    var words = text.split(meow)
    for (var i = 0; i < words.length ; i++) {
        var word = words[i]
        var uni16 = ""
        if(word != ""){
            for (var j = 0; j < word.length; j++) {
                switch(word.charCodeAt(j))
                {
                case 8251:
                    uni16 = uni16 + '0'
                    break
                case 9651:
                    uni16 = uni16 + '1'
                    break
                case 9671:
                    uni16 = uni16 + '2'
                    break
                case 9675:
                    uni16 = uni16 + '3'
                    break
                case 9678 :
                    uni16 = uni16 + '4'
                    break
                case 9679:
                    uni16 = uni16 + '5'
                    break
                case 9734 :
                    uni16 = uni16 + '6'
                    break
                case 9733:
                    uni16 = uni16 + '7'
                    break
                case 12290:
                    uni16 = uni16 + '8'
                    break
                case 21596:
                    uni16 = uni16 + '9'
                    break
                case 21714 :
                    uni16 = uni16 + 'a'
                    break
                case 21780 :
                    uni16 = uni16 + 'b'
                    break
                case 26114:
                    uni16 = uni16 + 'c'
                    break
                case 65281:
                    uni16 = uni16 + 'd'
                    break
                case 65311:
                    uni16 = uni16 + 'e'
                    break
                case 65374:
                    uni16 = uni16 + 'f'
                    break

                }
            }
            if(uni16 != ""){
                var int10 = parseInt(uni16, 16)
                if(int10 != NaN){
                    res = res + String.fromCharCode(int10)
                }
            }
        }
    }
    if(res == ""){
        res = "啊咧咧，结果为空，肯定是哪里有问题哦QAQ...The result is empty, there must be something wrong QAQ..."
    }
    return res
}