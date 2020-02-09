"""
Классы для отображения и хранения информации о игровом поле
"""

class SudoLine(object):
    """
    Класс для хранения столбцов/строк/квадратов
    """
    full_values_set = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    value_set = None
    def __init__(self, dimention = 3, overwrite = True):
        self.__dim = dimention
        if dimention < 2 or dimention > 5:
            self.__dim = 3
        self.value_set = set(self.full_values_set[:self.__dim*self.__dim])
        self.__current_set = set(list(self.value_set))
        self.__line = [None for i in range(self.__dim* self.__dim)]
        self.overwrite = overwrite

    @property
    def dim(self):
        """
        Свойство, содержащее число измерений нашего судоку
        """
        return self.__dim

    @property
    def values(self):
        """
        Возвращает список с заполнеными значениями
        """
        return self.__line

    @property
    def current_set(self):
        """
        Возвращает текущие допустимые значения символов для вставки (неотгаданные символы) Type = set
        """
        return self.__current_set

    def can_insert(self, symbol, position):
        """Проверяет на возможность вставки символа в указанную позицию

        Arguments:
            symbol {String} -- [Вставляемый символ]
            position {Integer} -- [Позиция для вставки. Нумерация с единицы!]

        Returns:
            [Integer] -- [0 - символ не относится к числу допустимых; 1 - символ допустим, но позиция занята;
            2 - символ допустим и позиция для вставки свободна]
        """
        if symbol not in self.__current_set:
            return 0
        if self.__line[position-1] is not None:
            return 1
        return 2

        
    def insert(self, symbol, position):
        """
        Метод вставляет символ в указанную позицию, если это допустимо
        
        Arguments:
            symbol {[string]} -- [символ для вставки]
            position {[int]} -- [позиция для вставки (номерация с единицы)]
        
        Returns:
            [type] -- [description]
        """
        state = self.can_insert(symbol,position)
        if not state:
            return (False, state, "Символ не допустим")
        if state == 1 and not self.overwrite:
            return (False, state, "Позиция уже занята и автозамена отключена")
        if state == 2:
            self.values[position-1] = symbol
            self.__current_set.remove(symbol)
            return (True, state, "Символ вставлен в пустую позицию")
        if state == 1 and self.overwrite:
            self.__current_set.add(self.values[position-1])
            self.values[position-1] = symbol
            self.__current_set.remove(symbol)
            return (True, state, "Символ заменен")
        return (False, -1, "Что-то пошло не там при обработке")
        
    def delete(self, position):
        """
        Удаление символа из указанной позиции        
        Arguments:
            position {[integer]} -- [Номер позиции символа. Нумерация с единицы!]
        
        Returns:
            [bool] -- [True - удаление было совершено; False - ничего удалено не было]
        """
        if position > len(self.values) or position < 1:
            return False
        if self.values[position-1] is not None:
            self.__current_set.add(self.values[position-1])    
            self.values[position-1] = None
            return True
        return False

    def to_str(self, wide = False):
        """
        преобразует значения в строку для вывода поля игры в консоль        
        Keyword Arguments:
            wide {bool} -- [Делает поле шире в случае True] (default: {False})
        
        Returns:
            {string} -- [Строка для печати поля]
        """
        if wide:
            sep = " | "
        else:
            sep = "|"
        out = sep
        for i in self.values:
            if i is None:
                out += " "
            else:
                out += i
            out += sep
        return out

    def __str__(self):
        """
        Вывод функции print()
        """
        return ("Размерность: "+ str(self.__dim) + "\n" + "Набор символов: " + str(self.value_set) + "\n")

class Board(object):
    """Класс описывает и отображает игровое поле
    """
    h_head = list("abcdefghijklmnopqrstuvwxyz")
    v_head = [i+1 for i in range(25)]
    sep_line = "+-"
    sep_line_w = "+---"

    def __init__(self, dimention = 3, overwrite = True):
        self.__dim = dimention
        if dimention < 2 or dimention > 5:
            self.__dim = 3
        self.overwrite = overwrite
        self.main_lines = [SudoLine(dimention , overwrite)]*(self.__dim*self.__dim)
        self.v_lines = [SudoLine(self.__dim, self.overwrite) for i in range(self.__dim*self.__dim)]
        self.sq_lines = [SudoLine(self.__dim, self.overwrite) for i in range(self.__dim*self.__dim)]

    @staticmethod
    def index_from_mark(col_head, row_head):
        """Преобразует значение метки в координаты доски
        
        Arguments:
            row_head {integer or string} -- метка столбца доски
            col_head {integer or string} -- метка строки доски
        
        Returns:
            tuple of integers -- Кортеж в виде (номер строки, номер столбца) номера с нуля
        """
        out = [0,0]
        if isinstance(row_head) == isinstance(1):
            out[0] = row_head
        elif isinstance(row_head) == isinstance("str"):
            try:
                out[0] = int(row_head)
            except:
                pass
        if isinstance(col_head) == isinstance("str"):
            for i,l in enumerate(Board.h_head):
                if l == col_head:
                    out[1] = i
        if isinstance(col_head) == isinstance(1):
            out[1] = col_head
        return tuple(out)
        
    def index_to_sq(self, row_number, col_number):
        """Переводит индекс поля в номер квадрата и индекс внутри него
        
        Arguments:
            row_number {integer} -- Номер строки, начиная с единицы
            col_number {integer} -- Номер столбца, начиная с единицы
        
        Returns:
            tuple of integers or bool -- Кортеж вида (номер квадрата, позиция в квардате) или False при неудачном преобразовании
        """
        out = False
        sq_numb = int(row_number/self.__dim) * self.__dim + (1 + col_number/self.__dim)
        sq_pos = self.__dim * ((row_number - 1)%self.__dim) + ((col_number - 1)%self.__dim) + 1
        out = (sq_numb, sq_pos)
        return  out
    
    
    def set_line(self, line_number, line:list):
        """Записывает линию в поле
        
        Arguments:
            line_number {integer} -- Номер записываемой строки 
            line {list} -- записываемая строка в виде списка
        
        Returns:
            bool -- Индикатор удачной записи
        """
        out = True
        for i, s in enumerate(line):
            if s == "":
                self.main_lines[line_number-1].delete(i)
            else:
                ins = self.main_lines[line_number-1].insert(s,i)
                if not ins[0]:
                    out = False
        return out

    def print_board(self):
        """Возвращает строку для печати игрового поля
        
        Returns:
            string -- строка с игровым полем для вывода в консоль
        """
        out = ""
        head = "      "
        sep_line = "    " + Board.sep_line_w * (self.__dim * self.__dim) + "\r\n"
        for i,s in enumerate(Board.h_head):
            if i >= self.__dim*self.__dim:
                break
            head += s
            head += "   "
        out += head + "\r\n"
        out += sep_line
        for i,line in enumerate(self.main_lines):
            temp_line =  str(Board.v_head[i]) + " "*(1 + int(i<10)) + line.to_str(wide=True) + "\r\n"
            out += temp_line
            out += sep_line
        return out

    def can_insert(self, symbol, position):
        """Проверяет можно ли вставить символ в указанную позицию
        
        Arguments:
            symbol {String} -- Символ передаваемый в виде строки
            position {String} -- Позиция передаваемая в виде одной строки, например "a1" или "11"
        
        Returns:
            tuple(bool, int, String) -- Кортеж вида (bool - возможна ли замена
            int - код операции: -1 если произошла ошибка, 1 - замена возможна, 0 - замена не возможна
            String - Описание происходящего на человеческом русском)
        """
        try:
            row_number, col_number = Board.index_from_mark(position[0],position[1])
        except:
            return (False, -1, "Ошибка при интерпретации позиции")
        out = True
        if self.main_lines[row_number].can_insert(symbol,col_number + 1) >= (1 + int(self.overwrite)):
            out = False
        if self.v_lines[col_number].can_insert(symbol, row_number + 1) >= (1 + int(self.overwrite)):
            out = False
        try:
            sq_numb, sq_pos = self.index_to_sq(row_number+1,col_number+1)
        except:
            return (False, -1, "Ошибка интерпретации позиции")
        if self.sq_lines[sq_numb].can_insert(symbol, sq_pos + 1) >= (1 + int(self.overwrite)):
            out = False
        if out:
            return (out, int(out), "Добавление возможно")
        return (out, int(out), "Добавление не возможно")




if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    s3 = SudoLine(3)
    s2 = SudoLine(2)
    s4 = SudoLine(4)
    s5 = SudoLine(5)
    s6 = SudoLine(6)
    s0 = SudoLine(0)
    print(s2)
    print(s3)
    print(s4)
    print(s5)
    print(s6)
    print(s0)
    
