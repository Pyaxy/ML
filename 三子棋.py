Player = 'X'  # 玩家的标志
Opponent = 'O'  # 对手的标志

transform = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2)
}  # 建立玩家输入位置与矩阵坐标的对应关系


# 棋盘类
class Board:
    def __init__(self):
        self.board = [['-'] * 3 for _ in range(3)]  # 初始化棋盘，以二维数组来储存

    def check_winner(self):  # 遍历来判定胜负
        board = self.board

        # 判断横行是否胜利
        for i in range(3):
            if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
                if board[i][0] == Player:
                    return 10  # 如果X胜返回10
                elif board[i][0] == Opponent:
                    return -10  # O胜返回-10
        # 判断竖列是否胜利
        for i in range(3):
            if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
                if board[0][i] == Player:
                    return 10
                elif board[0][i] == Opponent:
                    return -10
        # 判断对角线是否胜利
        if (board[0][0] == board[1][1] and board[1][1] == board[2][2]) \
                or (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
            if board[1][1] == Player:
                return 10
            elif board[1][1] == Opponent:
                return -10
        return 0

    def is_left(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    return False  # 当出现'_'时没有结束棋局
        return True  # 遍历之后仍没有出现'_'，表明已经结束

    def display(self):  # 打印棋盘
        print("当前棋盘为：")
        for i in range(3):
            print(self.board[i][0], self.board[i][1], self.board[i][2])

    def is_legal_position(self, i, j):  # 判断棋盘的[i][j]位是否被占用
        if self.board[i][j] == '-':
            return True
        else:
            return False

    def move(self, action, player):  # 落子，第一个参数为落子位置，第二个参数为落子的内容
        self.board[action[0]][action[1]] = player

    def get_legal_action(self):  # 遍历棋盘得到所有合法的落子位置并返回其数组
        actions = []
        for i in range(3):
            for j in range(3):
                if self.is_legal_position(i, j):
                    actions.append((i, j))
        return actions


# 基本玩家类
class BasePlayer(object):
    def __init__(self, take='X'):
        self.take = take  # 玩家执的棋子类型，默认为X

    def move(self, board, action):  # 玩家落子
        board.move(action, self.take)

    def think(self, board):  # 玩家思考，在派生类中具体实现
        pass


# 人类玩家，继承于基本玩家
class Human(BasePlayer):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):  # 玩家思考
        while True:  # 永真循环，直到输入正确的数字
            position = int(input("请输入下一步棋(输入0-8的数字):"))  # 获得玩家落子位置
            try:
                action = transform[position]
                while not board.is_legal_position(action[0], action[1]):  # 直到输入合法落子位置
                    print("输入错误")
                    position = int(input("请输入下一步棋(输入0-8的数字):"))
                    action = transform[position]  # 把数字转换为坐标
                return action
            except:
                print("输入错误，请重新输入")


# AI玩家
class AIPlayer(BasePlayer):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):  # 玩家思考
        print("AI思考中...")
        take = ['X', 'O'][self.take == 'X']  # 得到与AI相反的标志
        player = AIPlayer(take)  #使用上述标志创建假想敌
        _, action = self.minimax(board, 0, player, -10000, 10000)  # Minimax算法来计算最佳落子
        print("AI选择了:", action)
        return action

    # minimax算法来计算最佳落子位置
    # 第一个参数为棋盘，第二个参数为深度，第三个参数为假想敌，第四个参数为alpha-beta剪枝中的下界，第五个参数为alpha-beta剪枝中的上届
    def minimax(self, board, depth, player, alpha, beta):
        if self.take == 'O':
            bestval = -10  # 初始化让局面值最小
        else:
            bestval = 10  # 初始化让局面值最大
        score = board.check_winner()  # 判断是否胜利
        if score == 10:
            return -10 + depth, None  # 人类赢了使值尽可能小
        elif score == -10:
            return 10 - depth, None  # AI赢了使值尽可能大
        elif board.is_left():
            return 0, None  # 返回0表示平局
        for action in board.get_legal_action():  # 遍历每一个合法走法
            board.move(action, self.take)  # 假设走一步
            val, _ = player.minimax(board, depth + 1, self, alpha, beta)  # 假想敌来想对策
            board.move(action, '-')  # 假设的一部消失

            if self.take == 'O':  # 得到最大值
                if val > bestval:
                    alpha = val
                    bestval, bestaction = val, action
                    if alpha > beta:
                        break
            else:  # 得到最小值
                if val < bestval:
                    beta = val
                    bestval, bestaction = val, action
                    if alpha > beta:
                        break
        return bestval, bestaction  # 返回最大值以及其行动


class Game:
    def __init__(self):
        self.board = Board()  # 游戏棋盘初始化
        self.current_player = None  # 现在执子一方

    def initialize_player(self, p, take='X'):  # 初始化玩家
        if p == 0:
            return Human(take)  # 0代表人类
        else:
            return AIPlayer(take)  # 1代表AI

    def switch_player(self, p1, p2):
        if self.current_player == None:  # 第一次进入循环时让p1执子
            return p1
        else:
            return [p1, p2][self.current_player == p1]  # 交换双方

    def run(self):
        print('\t\t--游戏开始--')
        p1 = int(input("请输入第一个玩家的属性(AI为1，真人为0):"))
        p2 = int(input("请输入第二个玩家的属性(AI为1，真人为0):"))
        player1 = self.initialize_player(p1, 'X')  # 初始化玩家1
        player2 = self.initialize_player(p2, 'O')  # 初始化玩家2
        self.board.display()  # 打印空棋盘
        while True:
            self.current_player = self.switch_player(player1, player2)  # 交换玩家
            action = self.current_player.think(self.board)  # 执子玩家思考
            self.board.move(action, self.current_player.take)  # 执子玩家落子
            self.board.display()  # 打印棋盘
            if self.board.check_winner() == 10:
                print("Player1胜利啦！")
                break
            elif self.board.check_winner() == -10:
                print("Player2胜利啦！")
                break
            elif self.board.is_left():
                print("你们不分上下噢")
                break


if __name__ == '__main__':
    Game().run()
