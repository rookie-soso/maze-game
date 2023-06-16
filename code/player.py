import pygame

class Player:
    def __init__(self, screen, cell_width, cell_height):
        self.screen = screen
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.x = 0
        self.y = 0

    def move(self, maze, direction):
        # 根据捕获到的键盘操作更新玩家的位置
        direction_map = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1),
        }
        dx, dy = direction_map[direction]
        nx = self.x + dx
        ny = self.y + dy

        # 玩家在迷宫内，且行进的方向没有墙阻挡
        if 0 <= nx < maze.rows and 0 <= ny < maze.cols:
            if direction == 'down' and maze.maze[self.x][self.y].down_wall:
                return
            elif direction == 'right' and maze.maze[self.x][self.y].right_wall:
                return
            elif direction == 'up' and maze.maze[nx][ny].down_wall:
                return
            elif direction == 'left' and maze.maze[nx][ny].right_wall:
                return
            self.x = nx
            self.y = ny

    def draw(self, chosen_player):
        # 绘制玩家
        player_x = self.y * self.cell_width
        player_y = self.x * self.cell_height
        # 选择了1号玩家就绘制玩家1的图片
        if chosen_player == 1:
            player_image1 = pygame.image.load(r"..\picture\player1_Yeri.png").convert_alpha()
            player_image1 = pygame.transform.scale(player_image1, (self.cell_width - 4, self.cell_height - 4))
            self.screen.blit(player_image1, (player_x + 2, player_y + 2))
        # 2号玩家
        elif chosen_player == 2:
            player_image2 = pygame.image.load(r"..\picture\player2_Poopy.png").convert_alpha()
            player_image2 = pygame.transform.scale(player_image2, (self.cell_width - 4, self.cell_height - 4))
            self.screen.blit(player_image2, (player_x + 2, player_y + 2))
        # 3号玩家
        elif chosen_player == 3:
            player_image3 = pygame.image.load(r"..\picture\player3_Lucas.png").convert_alpha()
            player_image3 = pygame.transform.scale(player_image3, (self.cell_width - 4, self.cell_height - 4))
            self.screen.blit(player_image3, (player_x + 2, player_y + 2))

        pygame.display.update()
