import unittest
import board

class LineTests(unittest.TestCase):
    """Тестовый набор для класса SudoLine
    
    Arguments:
        unittest {[type]} -- [description]
    """
    
    def setUp(self):        
        self.sudo_line = board.SudoLine()
        self.sudo_line2 = board.SudoLine(2)
        self.sudo_line4 = board.SudoLine(4)

    def test_dim(self):
        """Проверка размерности
        """
        self.assertEqual(self.sudo_line.dim, 3, "Проверка размерности по умолчанию")
        self.assertEqual(self.sudo_line2.dim, 2, "Проверка размерности 2")
        self.assertEqual(self.sudo_line4.dim, 4, "Проверка размерности 4")
    
    def test_current_set(self):
        """Проверка входящих символов
        """
        self.assertEqual(self.sudo_line.current_set, set("123456789"), "Проверка символов размерности по умолчанию")
        self.assertEqual(self.sudo_line2.current_set, set("1234"), "Проверка символов размерности 2")
        self.assertEqual(self.sudo_line4.current_set, set("123456789ABCDEFG"), "Проверка символов размерности 4")

    def test_values(self):
        """Проверка заполненных значений
        """
        self.assertEqual(self.sudo_line.values, [None for i in range(9)], "Проверка символов размерности по умолчанию")
        self.assertEqual(self.sudo_line2.values, [None for i in range(4)], "Проверка символов размерности 2")
        self.assertEqual(self.sudo_line4.values, [None for i in range(16)], "Проверка символов размерности 4")

    def test_can_insert(self):
        """Проверка функции на возможность вставки
        """
        self.assertEqual(self.sudo_line.can_insert("1", 2), 2, "Проверка на возможность вставки в пустую строку")
        self.sudo_line.insert("1",2)
        self.assertEqual(self.sudo_line.can_insert("2", 2), 1, "Проверка на возможность вставки в занятую позицию")
        self.assertEqual(self.sudo_line.can_insert("A", 3), 0, "Проверка вставки недопустимого символа")
        self.assertEqual(self.sudo_line.can_insert("1", 3), 0, "Проверка вставки вставленного символа символа")

    def test_insert(self):
        """Проверка возможности вставки
        """
        self.assertEqual(self.sudo_line.insert("1",1)[1], 2, "Проверка вставки в пустую строку")
        self.assertEqual(self.sudo_line.insert("1",1)[1], 0, "Проверка повторной вставки")
        self.assertEqual(self.sudo_line.insert("2",1)[1], 1, "Проверка заменяющей вставки")

    def test_delete(self):
        """Проверка возможности удаления
        """
        self.assertEqual(self.sudo_line.delete(2), False, "Проверка удаления из пустой позиции")
        self.sudo_line.insert("1", 2)
        self.assertEqual(self.sudo_line.delete(2), True, "Проверка удаления из занятой позиции")

    def test_to_str(self):
        """Проверка перевода в строку линии судоку
        """
        pass

class BoardTests(unittest.TestCase):
    """Тестовый набор для класса Board
    
    Arguments:
        unittest {[type]} -- [description]
    """
    def setUp(self):        
        self.tboard = board.Board()

    def test_board_constructor(self):
        """Тестирование класса вцелом
        """
        self.assertEqual(len(self.tboard.main_lines), 9, "Проверка количества строк")
        self.assertEqual(len(self.tboard.v_lines), 9, "Проверка количества столбцов")
        self.assertEqual(len(self.tboard.sq_lines), 9, "Проверка количества квадратов")

    def test_index_from_mark(self):
        """Проверка перевода метки в координатную позицию
        """
        self.assertEqual(board.Board.index_from_mark("a", "1"), (1,1), "Передача строк")
        self.assertEqual(board.Board.index_from_mark(1, 1), (1,1), "Передача чисел")
        self.assertEqual(board.Board.index_from_mark("a", 1), (1,1), "Передача строки и числа")
        self.assertEqual(board.Board.index_from_mark(1, "1"), (1,1), "Передача числа и строки")

    def test_index_to_sq(self):
        """Проверка перевода номеров строки и столбца в номер и позицию квадрата
        """
        self.assertEqual(self.tboard.index_to_sq(1,1), (1,1), "Верхний левый угол")
        self.assertEqual(self.tboard.index_to_sq(1,9), (3,3), "Верхний правый угол")
        self.assertEqual(self.tboard.index_to_sq(9,1), (7,7), "Нижний левый угол")
        self.assertEqual(self.tboard.index_to_sq(9,9), (9,9), "Нижний правый уго")
        self.assertEqual(self.tboard.index_to_sq(4,5), (5,2), "Вторая клетка из центрального квадрата")
        self.assertEqual(self.tboard.index_to_sq(10,10), False, "Перевод несуществующей позиции")

    def test_set_line(self):
        """Проверка записи линии
        функция находится в разработке
        """
        pass



if __name__ == "__main__":
    unittest.main()