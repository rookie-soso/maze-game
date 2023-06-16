from random import shuffle

import pygame


class Cell:
    # 单元格类，封装一个单元格信息，便于maze数组进行操作
    def __init__(self, x, y, down_wall=True, right_wall=True):
        self.x = x  # 单元格左上角位置
        self.y = y
        self.down_wall = down_wall   # 单元格的下边界，True代表没有打通
        self.right_wall = right_wall   # 单元格的右边界，True代表没有打通

class Maze:
    def __init__(self, screen, cell_width, cell_height, rows=30, cols=40):
        self.screen = screen
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.rows = rows
        self.cols = cols
        self.maze = [[None for j in range(cols)] for i in range(rows)]
        self.visited = [[None for j in range(cols)] for i in range(rows)]   # 辅助数组，存放0或1，代表单元格是否被遍历过

        # 初始化辅助访问数组与迷宫数组
        for i in range(rows):
            for j in range(cols):
                self.maze[i][j] = Cell(i, j)  # 数组里的每个元素都是一个cell对象，操作数组元素是在操作一个封装起来的类
                self.visited[i][j] = 0   # 0代表该位置没有被遍历过

    def generate(self, stack=[]):
        done = True  # 是否退出递归的条件
        # 检查所有单元格是否全被遍历
        for i in range(self.rows):
            for j in range(self.cols):
                if self.visited[i][j] == 0:
                    done = False
                    break
        # 如果辅助数组全部为1，代表迷宫生成完毕，可以退出递归
        if done:
            return

        # 开始栈为空，把二维数组左上角单元格放进栈（用列表实现）中
        if len(stack) == 0:
            stack.append(self.maze[0][0])

        cell = stack[-1]  # 栈顶元素

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(directions)
        for direction in directions:
            dx, dy = direction
            # 根据方向计算新的索引
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and not self.visited[nx][ny]:
                # 可能将要打通的单元格在二维数组内，且没有被遍历过
                self.visited[nx][ny] = 1   # 标记可能将会打通的单元格在辅助数组中的位置为1，代表已经被访问
                neighbor = self.maze[nx][ny]  # 把可能会打通的单元格记作neighbor
                stack.append(neighbor)  # 把neighbor单元格放进列表尾部
                if dx == 1 and dy == 0:
                    # 如果方向是（1,0），打通current单元格的下方墙壁
                    cell.down_wall = False
                elif dx == 0 and dy == 1:
                    # 如果方向是（0,1），打通current单元格的右方墙壁
                    cell.right_wall = False
                elif dx == -1 and dy == 0:
                    # 如果方向是（-1,0），打通neighbor单元格的下方墙壁
                    neighbor.down_wall = False
                elif dx == 0 and dy == -1:
                    # 如果方向是（0，-1），打通neighbor单元格的右方墙壁
                    neighbor.right_wall = False
                self.generate(stack)

    def draw(self):
        background_image = pygame.image.load(r"..\picture\maze_background.jpg")
        background_image = pygame.transform.scale(background_image, (800, 600))
        self.screen.blit(background_image, (0, 0))


        for x in range(self.cols):
            for y in range(self.rows):
                if self.maze[y][x].down_wall:
                    # 这里在二维数组中的坐标需要转置一下再对应到游戏界面上去
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     (x * self.cell_width, y * self.cell_height + self.cell_height),
                                     (x * self.cell_width + self.cell_width,
                                      y * self.cell_height + self.cell_height), width = 3)
                if self.maze[y][x].right_wall:
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     (x * self.cell_width + self.cell_width, y * self.cell_height),
                                     (x * self.cell_width + self.cell_width,
                                      y * self.cell_height + self.cell_height), width = 3)

        exit_image = pygame.image.load(r"..\picture\exit.png").convert_alpha()
        exit_image = pygame.transform.scale(exit_image, (self.cell_width - 4, self.cell_height - 4))
        self.screen.blit(exit_image, ((self.cols - 1) * self.cell_width + 2, (self.rows - 1) * self.cell_height + 2))
        pygame.display.update()
