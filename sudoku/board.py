"""
Класс для решения судоку
"""

class SudoLine(object):
    """
    Класс для хранения столбцов/строк/квадратов
    """
    full_values_set = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    value_set = None
    def __init__(self, dimention = 3):
        self.__dim = dimention
        if dimention < 2 or dimention > 5:
            self.__dim = 3
        self.value_set = set(self.full_values_set[:self.__dim*self.__dim])
        
        
    @property
    def dim(self):
        """
        Свойство, содержащее число измерений нашего судоку
        """
        return self.__dim
    
    def __str__(self):
        """
        Вывод функции print()
        """
        return ("Размерность: "+ str(self.__dim) + "\n" + "Набор символов: " + str(self.value_set) + "\n")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
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
