import sys


class Solver:
    def __init__(self):
        self.t = 2
        self.rightshift = False

        # Variant 73
        # F = (x^4+x+1)*(x^4+x^3+x^2+x+1) = x^8 + x^7 + x^6 + 2x^5 + 3x^4 + 2x^3 + 2x^2 + 2x + 1 = x^8 + x^7 + x^6 + x^4 + 1 = 111010001
        self.notE = "011001110011011"
        self.F = "111010001"

    def div(self, divident: str, divider: str):
        print(divident)
        tmp = int(divident, 2) >> len(str(divident)) - len(str(divider))
        divident_len = len(divident)
        divider_len  = len(divider)
        divider = int(divider,2)
        i = 1
        remainder = []
        quotient = ""
        while (i != divident_len - divider_len + 2):
            zeros = 0b0
            zerosstr = "0"
            while(len(zerosstr) != divider_len):
                zerosstr += "0"
            dividerstr = str(bin(divider))[2:]
            check = tmp & (1 << (divider_len - 1)) == 0
            tmp = tmp ^ zeros if check else tmp ^ divider
            remainder.append(tmp)
            strtmp = str(bin(tmp))
            strtmp = strtmp[2:]
            strtmp = strtmp + divident[divider_len - 1 + i:divider_len - 1 + i + 1]
            tmp = int(strtmp,2)
            while(len(strtmp) != divider_len):
                strtmp = "0" + strtmp
            for _ in range(i-1):
                if (check):
                    zerosstr = ' ' + zerosstr
                else:
                    dividerstr = ' ' + dividerstr
            if (i != divident_len - divider_len + 1):
                for _ in range(i):
                    strtmp = ' ' + strtmp
            else:
                strtmp = strtmp[1:]
                for _ in range(i):
                    strtmp = ' ' + strtmp
            if (check):
                print(zerosstr)
                quotient += "0"
            else:
                print(dividerstr)
                quotient += "1"
            print(strtmp)
            i += 1
        print(f"\nЧастное: {quotient}\n")
        return tmp, remainder

    def run(self):
        print(f"~E = {self.notE}")
        print(f"F = {self.F}")
        self.shiftcounter = 0
        noteEtmp = self.notE
        check = False
        print("~E/F")
        while(check == False and self.shiftcounter != len(self.notE)):
            tmp, remainder = self.div(divident = noteEtmp, divider = self.F)
            if (bin(tmp).count("1") <= self.t):
                print(f"Кратность ошибки: t = {self.t}")
                print(f'w(R(x)) = {bin(tmp).count("1")} <= t')
                check = True
            else:
                noteEtmp = noteEtmp[len(noteEtmp) - 1:] + noteEtmp[:len(noteEtmp) - 1] if self.rightshift else noteEtmp[1:] + noteEtmp[:1]
                self.shiftcounter += 1
                print(f"Кратность ошибки: t = {self.t}")
                print(f'w(R(x)) = {bin(tmp).count("1")} > t')
                if (self.shiftcounter != len(self.notE)):
                    print(f"Сдвигаем ~E на {self.shiftcounter} {'вправо' if self.rightshift else 'влево'}:")
        if (self.shiftcounter == len(self.notE)):
            print("\nОшибку найти не удалось!")
            return
        print("Ошибка найдена!")
        print(f"Потребовалось сдвигов: {self.shiftcounter}")
        print("\nИсправляем ошибку:")
        self.E = int(noteEtmp, 2) ^ tmp
        self.E = str(bin(self.E))[2:]
        while(len(self.E) != len(self.notE)):
            self.E = "0" + self.E
        print(f"{noteEtmp} xor {str(bin(tmp))[2:]} = {self.E}")
        if (self.shiftcounter > 0):
            print(f"\nСдвигаем {'влево' if self.rightshift else 'вправо'} на {self.shiftcounter}:")
            for _ in range(self.shiftcounter):
                self.E = self.E[1:] + self.E[:1] if self.rightshift else self.E[len(self.E) - 1:] + self.E[:len(self.E) - 1]
        print(f"Исходный E: {self.E}")
        rev = self.E[:-len(self.F) + 1]
        rev = rev[::-1]
        print(f"И: {rev}, в десятичном виде: {int(rev, 2)}")
        tmpstr = bin(tmp)
        tmpstr = tmpstr[2:]
        while (len(tmpstr) != len(self.notE)):
            tmpstr = "0" + tmpstr
        for _ in range(self.shiftcounter):
            tmpstr = tmpstr[1:] + tmpstr[:1] if self.rightshift else tmpstr[len(tmpstr) - 1:] + tmpstr[:len(tmpstr) - 1]
        errvec = tmpstr
        errvec = errvec[errvec.find("1"):]
        print(f"Вектор e: {errvec}, в восьмеричном виде: {oct(int(errvec, 2))}")
        print("\nПроверим найденное число И:")
        print("Посчитаем образующую матрицу:")
        genmat_divident = "1"
        while (len(genmat_divident) != len(self.notE)):
            genmat_divident += "0"
        tmp, remainder = self.div(divident = genmat_divident, divider = self.F)
        tranones = "1"
        while (len(tranones) != len(self.notE) - len(self.F) + 1):
            tranones = "0" + tranones
        for r in remainder:
            rstr = str(bin(r))[2:]
            while (len(rstr) != len(self.F) - 1):
                rstr = "0" + rstr
            print(f"{tranones} | {rstr}")
            tranones = tranones[1:] + tranones[:1]
        print("\nВычисляем b:")
        bcounter = 0
        acounter = 0
        bArr = []
        while (len(bArr) != len(self.F) - 1):
            bArr.append(0)
        bcolumn = []
        while (len(bcolumn) != len(self.F) - 1):
            bcolumn.append("")
        for b in bArr:
            for r in remainder:
                rstr = str(bin(r))[2:]
                while (len(rstr) != len(self.F) - 1):
                    rstr = "0" + rstr
                bcolumn[bcounter] = bcolumn[bcounter] + rstr[bcounter]
                if (int(bcolumn[bcounter][acounter]) & 1 == 1):
                    b ^= int(rev[acounter])
                acounter += 1
            bArr[bcounter] = b
            bcounter += 1
            acounter = 0
            print(f"b{bcounter} = {b}")
        E1 = rev[::-1]
        for b in bArr:
            E1 = E1 + str(b)
        notE1 = int(E1, 2) ^ int(errvec, 2)
        notE1 = str(bin(notE1))[2:]
        while (len(notE1) != len(self.notE)):
            notE1 = "0" + notE1
        print(f"\nE1 = {E1}")
        print(f"Добавляем ошибку:")
        print(f"{E1} xor {errvec} = {notE1}")
        print(f"~E1 = {notE1}")
        print(f"~E  = {self.notE}")
        if (notE1 == self.notE):
            print("~E1 равен ~E, ответ верный.")
        else:
            print("Ой-ой...")

def main(argv):
    solver = Solver()
    solver.run()

if __name__ == "__main__":
    main(sys.argv[1:])
