import sys

import pygame
from pygame.locals import *

from maze import Maze
from player import Player

#游戏类
class Game:
    def __init__(self):
        pygame.init()
        self.window_size = (600, 600)  # 游戏窗口大小
        self.chosen_player = 0
        self.screen = pygame.display.set_mode(self.window_size)
        self.font1 = pygame.font.Font(r"..\font\AaMaKeTi-2.ttf", 28)  # 导入字体
        self.font2 = pygame.font.Font(r"..\font\AaMaKeTi-2.ttf", 12)
        pygame.display.set_caption('迷宫游戏')   # 设置游戏标题

    def start(self):
        pygame.mixer.init()
        sound1 = pygame.mixer.Sound(r"..\music\start.wav")
        sound2 = pygame.mixer.Sound(r"..\music\level.mp3")
        sound3 = pygame.mixer.Sound(r"..\music\end2.mp3")

        sound2.play(-1)
        self.start_screen()   # 展示开始游戏界面
        self.choose_player()  # 选择玩家界面
        self.start_time = pygame.time.get_ticks()  # 开始计时
        self.start_maze(8, 8, 1)   # 第一关
        self.start_maze(10, 10, 2)   # 第二关
        self.start_maze(12, 12, 3)   # 第三关
        self.end_screen()   # 展示结束游戏界面
        sound2.stop()
        sound3.play()
        self.congratulation_screen()  # 展示烟花动画
        sound3.stop()
    def start_maze(self, maze_rows, maze_cols, n):
        self.cell_width = self.window_size[0] / maze_cols   # 迷宫单元格宽度
        self.cell_height = self.window_size[1] / maze_rows  # 迷宫单元格高度
        self.maze = Maze(self.screen, self.cell_width, self.cell_height, maze_rows, maze_cols)
        self.maze.generate()  # 加载迷宫地图
        self.maze.draw()    # 画迷宫
        self.player = Player(self.screen, self.cell_width, self.cell_height)
        self.player.draw(self.chosen_player)   # 画玩家
        self.draw_info(n)    # 绘制关卡信息
        self.play(n)

    def choose_player(self):
        running = True
        # 绘制背景
        choose_player_image = pygame.image.load(r"../picture/choose_player_background.jpg")
        choose_player_image = pygame.transform.scale(choose_player_image, (self.window_size[0], self.window_size[1]))
        self.screen.blit(choose_player_image, (0, 0))
        # 绘制  选择玩家  信息
        self.screen.blit(pygame.font.Font(r"..\font\AaMaKeTi-2.ttf", 50).render("请选择玩家", True, (255, 255, 255)),
                         (180, 40))
        # 绘制玩家1
        player1_image = pygame.image.load(r"../picture/player1_Yeri.png")
        player1_image = pygame.transform.scale(player1_image, (100, 100))
        self.screen.blit(player1_image, (75, 250))
        # 绘制玩家2
        player2_image = pygame.image.load(r"../picture/player2_Poopy.png")
        player2_image = pygame.transform.scale(player2_image, (100, 100))
        self.screen.blit(player2_image, (250, 250))
        # 绘制玩家3
        player3_image = pygame.image.load(r"../picture/player3_Lucas.png")
        player3_image = pygame.transform.scale(player3_image, (100, 100))
        self.screen.blit(player3_image, (425, 250))
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    if 75 <= event.pos[0] <= 175 and 250 <= event.pos[1] <= 350:
                        self.chosen_player = 1
                        running = False
                    if 250 <= event.pos[0] <= 350 and 250 <= event.pos[1] <= 350:
                        self.chosen_player = 2
                        running = False
                    if 425 <= event.pos[0] <= 525 and 250 <= event.pos[1] <= 350:
                        self.chosen_player = 3
                        running = False

                    pygame.display.flip()  # 刷新屏幕

    def start_screen(self):
        running = True
        button_pos = (self.window_size[0] // 2 - 100, self.window_size[1] // 2 + 100)    # 设置开始游戏的按钮背景位置坐标
        background_image = pygame.image.load(r"../picture/start_background.jpg")   # 加载开始界面图片
        background_image = pygame.transform.scale(background_image, (self.window_size[0], self.window_size[1]))  # 压缩到游戏窗口大小
        button_image = pygame.image.load(r"..\picture\PlayButton.png")
        button_image = pygame.transform.scale(button_image, (200, 100))
        self.screen.blit(background_image, (0, 0))  # 把背景图片绘制到屏幕上
        self.screen.blit(button_image, (200, 400))
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    # 捕获到鼠标事件后才退出循环
                    if button_pos[0] <= event.pos[0] <= button_pos[0] + 200 and \
                            button_pos[1] <= event.pos[1] <= button_pos[1] + 100:
                        running = False

            self.screen.blit(pygame.font.Font(r"..\font\AaMaKeTi-2.ttf", 50).render("Mystic Labyrinth", True, (255, 255, 255)),
                             (60, 40))
            pygame.display.flip()  # 刷新屏幕

    def congratulation_screen(self):
        # 背景
        congratulation_image = pygame.image.load(r"..\picture\congratulation_screen.jpg")
        congratulation_image = pygame.transform.scale(congratulation_image, (self.window_size[0], self.window_size[1]))
        self.screen.blit(congratulation_image, (0, 0))

        # 动态图像处理
        file_format = r"..\fire\{}.png"  # 定义动态图像的文件名格式，从0到49
        # 加载五十帧动态图像并存储在列表中
        frames = []
        for i in range(50):
            frame = pygame.image.load(file_format.format(i)).convert_alpha()
            frame = pygame.transform.scale(frame, (150, 150))
            frames.append(frame)
        current_frame = 0  # 当前帧索引
        clock = pygame.time.Clock()

        # 祝贺信息
        self.screen.blit(pygame.font.Font(r"..\font\AaMaKeTi-2.ttf", 25).render("CONGRATULATIONS! YOU WIN!", True, (255, 255, 255)),
                         (60, 500))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

            self.screen.blit(frames[current_frame], (226, 50))  #  绘制当前帧
            clock.tick(8)  # 控制帧率
            current_frame = (current_frame + 1) % len(frames)
            pygame.display.flip()  # 刷新屏幕

    def end_screen(self):
        running = True
        # 背景
        background_image = pygame.image.load(r"..\picture\end_background.jpg")   # 加载背景图片
        background_image = pygame.transform.scale(background_image, (self.window_size[0], self.window_size[1]))
        self.screen.blit(background_image, (0, 0))  # 绘制背景图片
        # 按钮
        next_button_image = pygame.image.load(r"..\picture\next_button.png")  # 加载背景图片
        next_button_image = pygame.transform.scale(next_button_image, (130, 100))
        self.screen.blit(next_button_image, (370, 400))
        time = (pygame.time.get_ticks() - self.start_time) / 1000  # 计算总时长

        # 时间排行
        time_list = []
        # 把文件中的时间数据一行一行读出来，并添加到时间列表中
        with open("record.txt", "r", encoding='utf-8') as f1:
            data = f1.readline()
            while data:
                time_list.append(float(data))
                data = f1.readline()

        # 把本轮时间信息添加到时间文件中
        with open("record.txt", 'a', encoding='utf-8') as f2:
            f2.write(str(time) + '\n')

        # 把本轮时间信息加入到时间列表中
        time_list.append(time)
        sorted_time_list = sorted(time_list)
        rank = sorted_time_list.index(time) + 1
        distance = rank - 1
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    if 370 <= event.pos[0] <= 500 and 400 <= event.pos[1] <= 500:
                        running = False

            self.screen.blit(self.font1.render(f'本轮共计用时： {time}S', True, (255, 165, 0)),
                             (140, 50))  # 绘制时长信息

            # 如果文件中有时间信息
            if time_list:
                if rank == 1:
                    # 如果此轮用时在所有记录中最快，提示“达成新纪录”
                    self.screen.blit(self.font1.render('达成新纪录！', True, (255, 165, 0)), (140, 90))
                else:
                    self.screen.blit(self.font1.render(f'最高记录： {sorted_time_list[0]}S', True, (255, 165, 0)), (140, 90))
                    self.screen.blit(self.font1.render(f'距离最高记录还差 {distance} 位', True, (255, 165, 0)), (140, 130))

            #  如果文件中没有时间信息，即第一次启动游戏
            else:
                self.screen.blit(self.font1.render('达成新纪录！', True, (255, 165, 0)), (140, 90))

            pygame.display.flip()

    def play(self, n):
        running = True
        self.clock = pygame.time.Clock()
        while running:
            self.maze.draw()
            self.player.draw(self.chosen_player)
            self.draw_info(n)

            self.clock.tick(10)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        self.player.move(self.maze, 'down')
                    if event.key == K_UP:
                        self.player.move(self.maze, 'up')
                    if event.key == K_LEFT:
                        self.player.move(self.maze, 'left')
                    if event.key == K_RIGHT:
                        self.player.move(self.maze, 'right')

            # 如果移动到出口位置，进入下一关
            if self.player.x == self.maze.cols - 1 and self.player.y == self.maze.rows - 1:
                running = False

    def draw_info(self, n):
        self.screen.blit(self.font2.render(f'LEVEL {n}', True, (117, 90, 87)), (540, 10))
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.start()