"""
Файл содержит классы и методы для консольной игры
"""
import  board

class Game():
    """
    Класс консольной игры в судоку
    """
    HELP_LITERAL = """Допустимые команды:
    q - выход;
    p - вывод игрового поля;
    i symbol pos - вставить символ symbol в позицию pos;
    c symbol pos - проверка возможности вставки символа symbol в позицию pos
    d pos - удаление символа из позиции pos;
    h - справка по игре. 
    (Позиция pos задается без пробела, например a1 или b3)
    """
    SHORT_HELP = "Выберите действие. Введите h для вывода справки: "
    
    def __init__(self, dimension = 3):
        self.__dim = dimension
        self.board = board.Board(dimention = self.__dim)
        self.exit = False
        
        
    def exec_command(self, command):
        """
        Выполнение команды с возвращением результата
        """
        out = None
        if not isinstance(command, list):
            #print("Команда не распознана")
            return None
        if command[0].lower().startswith("q"):
            out = "q"
        if command[0].lower().startswith("p"):
            print(self.board.print_board())
            out = "p"
        if command[0].lower().startswith("h"):
            print(Game.HELP_LITERAL)
            out = "h"
        if command[0].lower().startswith("d") and len(command) == 2:
            com = self.board.delete(command[1])
            if com is None:
                return None
            print(com)
            out = "d"
        if command[0].lower().startswith("c") and len(command) == 3:
            com = self.board.can_insert(command[1], command[2])
            print(com)
            out = "c"
        if command[0].lower().startswith("i"):
            com = self.board.insert(command[1], command[2])
            print(com)
            out = "i"
        return out
            
        
    def input_command(self):
        """Ввод и обработка команды пользователя
        """
        command_str = input(Game.SHORT_HELP)
        if command_str:
            command_list = command_str.split()
            if len(command_list) > 3:
                return command_list[:3]
            return command_list
        return None
        
    def game_start(self):
        """
        Запускает игровой цикл
        """
        while True:
            command = self.input_command()
            if not command:
                print("Команда не обработана")
                continue
            rezult = self.exec_command(command)
            print("Команда отправлена на выполнение")
            # здесь должна быть проверка на окончание игры, если командой являлась вставка
            if rezult == "q":
                self.exit = True
            if self.exit:
                exit_flag = input("Вы действительно хотите выйти из игры? y / n")
                if exit_flag.lowcase().startswith("y"):
                    break
                self.exit = False
                
            
if __name__ == "__main__":
    print("Создаю экземпляр игры")
    gm = Game()
    print("Запускаю игровой процесс")
    gm.game_start()
