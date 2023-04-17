import sys
import os
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


from typing import Optional
import arcade
import arcade.gui

SCREEN_TITLE = "ZOBMEN"

SPRITE_IMAGE_SIZE = 128

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_TILES = 0.5

SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRAVITY = 1500

DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

PLAYER_MASS = 2.0

PLAYER_MAX_HORIZONTAL_SPEED = 200
PLAYER_MAX_VERTICAL_SPEED = 4000

PLAYER_MOVE_FORCE_ON_GROUND = 8000
PLAYER_MOVE_FORCE_IN_AIR = 900
PLAYER_JUMP_IMPULSE = 1100

DEAD_ZONE = 0.1

RIGHT_FACING = 0
LEFT_FACING = 1

DISTANCE_TO_CHANGE_TEXTURE = 20

TILE_SIZE = 32


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_image = arcade.load_texture('background.jpg')
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.image_person = arcade.load_texture('sprite.png', flipped_horizontally=True)
        self.image_brain = arcade.load_texture('brain_main.png')

        self.v_box = arcade.gui.UIBoxLayout()

        # Название игры
        game_name = arcade.gui.UITextArea(text='ZOBMEN', font_name='Times New Roman', font_size=71,
                                          text_color=[255, 0, 0], height=100)
        self.v_box.add(game_name.with_space_around(bottom=80))

        # Кнопка start
        start_button = arcade.gui.UIFlatButton(text='Start Game', width=300)
        self.v_box.add(start_button.with_space_around(bottom=20))

        # Кнопка levels
        level_button = arcade.gui.UIFlatButton(text='Levels', width=300)
        self.v_box.add(level_button.with_space_around(bottom=20))

        # Кнопка exit
        exit_button = arcade.gui.UIFlatButton(text='Exit', width=300)
        exit_button.on_click = self.exit_game
        self.v_box.add(exit_button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center_x',
                anchor_y='center_y',
                child=self.v_box
            )
        )

        # Нажатие на кнопку start
        @start_button.event('on_click')
        def start_game(event):
            self.clear()
            game_view = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            game_view.setup()
            self.window.show_view(game_view)
            self.manager.clear()

        # Нажатие на кнопку levels
        @level_button.event('on_click')
        def level_game(event):
            self.clear()
            game_view = LevelView()
            self.window.show_view(game_view)
            self.manager.clear()

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        self.image_person.draw_scaled(center_x=100, center_y=150, scale=0.7, angle=-45)
        self.image_brain.draw_scaled(center_x=1200, center_y=150, scale=0.5, angle=25)
        self.manager.draw()

    # Нажатие на кнопку exit
    def exit_game(self, event):
        message_box = arcade.gui.UIMessageBox(width=400,
                                              height=400,
                                              message_text='Вы уверены, что хотите выйти?',
                                              callback=self.user_pressed,
                                              buttons=['Да', 'Нет'])
        self.manager.add(message_box)

    # Callback функция для кнопки exit
    def user_pressed(self, button_text):
        if button_text == 'Да':
            arcade.close_window()
        elif button_text == 'Нет':
            pass


class LevelView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_image = arcade.load_texture('background.jpg')
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        # Кнопка level 1
        level_button = arcade.gui.UIFlatButton(text='Level 1', width=300)
        self.v_box.add(level_button.with_space_around(bottom=20))

        # Кнопка level 2
        level2_button = arcade.gui.UIFlatButton(text='Level 2', width=300)
        level2_button.on_click = self.level2_game
        self.v_box.add(level2_button.with_space_around(bottom=20))

        # Кнопка level 3
        level3_button = arcade.gui.UIFlatButton(text='Level 3', width=300)
        level3_button.on_click = self.level2_game
        self.v_box.add(level3_button.with_space_around(bottom=20))

        # Кнопка level 4
        level4_button = arcade.gui.UIFlatButton(text='Level 4', width=300)
        level4_button.on_click = self.level2_game
        self.v_box.add(level4_button.with_space_around(bottom=20))

        # Кнопка level 5
        level5_button = arcade.gui.UIFlatButton(text='Level 5', width=300)
        level5_button.on_click = self.level2_game
        self.v_box.add(level5_button.with_space_around(bottom=250))

        # Кнопка exit
        exit_button = arcade.gui.UIFlatButton(text='Menu', width=300, y=20)
        exit_button.on_click = self.exit_game
        self.v_box.add(exit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center_x',
                anchor_y='center_y',
                child=self.v_box
            )
        )

        # Нажатие на кнопку level 1
        @level_button.event('on_click')
        def level_game(event):
            self.clear()
            game_view = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            game_view.setup()
            self.window.show_view(game_view)
            self.manager.clear()

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        self.manager.draw()

    # Нажатие на кнопку exit
    def exit_game(self, event):
        self.clear()
        game_view = StartView()
        self.window.show_view(game_view)
        self.manager.clear()

    # Callback функция для кнопки exit
    def user_pressed(self, button_text):
        if button_text == 'Да':
            self.clear()
            game_view = StartView()
            self.window.show_view(game_view)
            self.manager.clear()
        elif button_text == 'Нет':
            pass

    # Нажатие на кнопку level 2 - level 5
    def level2_game(self, event):
        message_box = arcade.gui.UIMessageBox(width=400,
                                              height=400,
                                              message_text='Coming soon...',
                                              buttons=['ОK'])
        self.manager.add(message_box)


class GridSprite(arcade.Sprite):  # 1
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/grassMid.png')


class GrassSprite(arcade.Sprite):  # 2
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/grassCenter.png')


class SpikesSprite(arcade.Sprite):  # 3
    def __init__(self):
        super().__init__()

        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/spikes.png')


class LavaSprite(arcade.Sprite):  # 4
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/lava.png')


class LavaHighSprite(arcade.Sprite):  # 5
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/lavaTop_high.png')


class GrassHillLeftSprite(arcade.Sprite):  # 6
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/grassHill_left.png')


class GrassHillRightSprite(arcade.Sprite):  # 7
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/grassHill_right.png')


class GrassCliffRightSprite(arcade.Sprite):  # 8
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/grassCliff_right.png')


class GrassCliffLeftSprite(arcade.Sprite):  # 9
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/grassCliff_left.png')


class SnowSprite(arcade.Sprite):  # 10
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/snowMid.png')


class SnowCliffRightSprite(arcade.Sprite):  # 11
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/snowCliff_right.png')


class SnowCliffLeftSprite(arcade.Sprite):  # 12
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/snowCliff_left.png')


class DoorMidSprite(arcade.Sprite):  # 13
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/doorClosed_mid.png')


class DoorTopSprite(arcade.Sprite):  # 14
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER / 2
        self.texture = arcade.load_texture(':resources:images/tiles/doorClosed_top.png')


class CoinSprite(arcade.Sprite):  # 15
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER
        self.texture = arcade.load_texture('brain.png')


class KeySprite(arcade.Sprite):  # 16
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER
        self.texture = arcade.load_texture(':resources:images/items/keyYellow.png')


class PlayerSprite(arcade.Sprite):

    def __init__(self, hit_box_algorithm):
        super().__init__()

        self.dead = None
        self.scale = SPRITE_SCALING_PLAYER

        main_path = ":resources:images/animated_characters/zombie/zombie"

        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle.png",
                                                          hit_box_algorithm=hit_box_algorithm)
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")

        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

        self.hit_box = self.texture.hit_box_points

        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0

        self.x_odometer = 0
        self.y_odometer = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometer += dx
        self.y_odometer += dy

        if not is_on_ground:
            if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
                self.y_odometer = 0
                self.cur_texture += 1

            if self.cur_texture > 1:
                self.cur_texture = 0
            return

        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return

        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:

            self.x_odometer = 0

            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

    def die(self):
        self.dead = True


class GameWindow(arcade.View):
    def __init__(self, width, height, title):

        super().__init__()

        self.door_list = None
        self.game_end = None
        self.game_win = False
        self.score_num = 0
        self.player_sprite: Optional[PlayerSprite] = None
        self.have_key = False

        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None
        self.kill_list: Optional[arcade.SpriteList] = None
        self.key_list: Optional[arcade.SpriteList] = None

        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.draw_need_key = False

        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None

        self.coin_sprite = None
        self.mushroom_sprite = None
        # Music
        self.background_music = None
        self.background_music_file = arcade.load_sound('music.mp3', True)

        # Music player
        self.player_music = None
        self.player_music_file = arcade.load_sound(':resources:sounds/jump5.wav', True)

        # Music coin
        self.coin_music = None
        self.coin_music_file = arcade.load_sound(':resources:sounds/coin5.wav', True)

        # Music gameover
        self.gameover_music = None
        self.gameover_music_file = arcade.load_sound('lose.wav', True)

        # Music win
        self.win_sound = None
        self.win_sound_file = arcade.load_sound('win_sound.wav', True)

        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Кнопка pause
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout(y=685)
        texture_pause_button = arcade.load_texture(':resources:onscreen_controls/flat_dark/pause_square.png')
        texture_pause_button_hovered = arcade.load_texture(':resources:onscreen_controls/shaded_light/pause_square.png')
        texture_pause_button_pressed = arcade.load_texture(':resources:onscreen_controls/shaded_dark/pause_square.png')
        pause_button = arcade.gui.UITextureButton(texture=texture_pause_button,
                                                  texture_hovered=texture_pause_button_hovered,
                                                  texture_pressed=texture_pause_button_pressed)
        self.v_box.add(pause_button.with_space_around(bottom=20, left=20))

        @pause_button.event('on_click')
        def pause_game(event):
            arcade.stop_sound(self.background_music)
            self.window.show_view(PauseView(self))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='left',
                anchor_y='left',
                child=self.v_box
            )
        )

        # def setup(self):
        # Сделал все в функции __init__ для того, чтобы работала пауза
        self.background_music = arcade.play_sound(self.background_music_file, 0.05, True, speed=0.7)

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.kill_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()

        map_plan = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 14, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 13, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             15, 0, 8, 1, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             11, 12, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 3, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 15, 0, 0, 0,
             0, 0, 15, 0, 0, 0, 2],
            [2, 0, 0, 0, 11, 10, 12, 0, 0, 11, 10, 10, 10, 10, 10, 10, 10, 12, 0, 0, 0, 11, 12, 0, 0, 11, 12, 0, 0, 0,
             11, 10, 12, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2],
            [2, 0, 15, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 2],
            [2, 1, 1, 9, 0, 0, 8, 9, 0, 0, 1, 0, 0, 8, 9, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 15, 0,
             0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1, 1, 9, 0, 0, 7, 1, 1, 1, 6,
             0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 15, 2],
            [2, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0,
             0, 1, 1, 1, 1, 2],
            [2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 6, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 9, 0, 0, 0, 7,
             2, 2, 2, 2, 2],
            [2, 0, 0, 0, 0, 0, 1, 2, 2, 2, 5, 5, 5, 2, 2, 2, 2, 2, 6, 0, 0, 0, 1, 0, 2, 5, 5, 2, 0, 0, 0, 0, 0, 0, 0, 2,
             2, 2, 2, 2, 2],
            [2, 0, 0, 0, 0, 1, 2, 2, 2, 2, 4, 4, 4, 2, 2, 2, 2, 2, 2, 6, 15, 0, 2, 5, 2, 4, 4, 2, 16, 0, 0, 0, 0, 0, 7,
             2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1],
        ]
        row_count = 22
        for row in map_plan:
            col_count = 0
            for tile in row:
                if tile == 1:
                    a = GridSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 2:
                    a = GrassSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 3:
                    a = SpikesSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.kill_list.append(a)
                elif tile == 4:
                    a = LavaSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.kill_list.append(a)
                elif tile == 5:
                    a = LavaHighSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.kill_list.append(a)
                elif tile == 6:
                    a = GrassHillLeftSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 7:
                    a = GrassHillRightSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 8:
                    a = GrassCliffLeftSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 9:
                    a = GrassCliffRightSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 10:
                    a = SnowSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 11:
                    a = SnowCliffLeftSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 12:
                    a = SnowCliffRightSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.wall_list.append(a)
                elif tile == 13:
                    a = DoorMidSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.door_list.append(a)
                elif tile == 14:
                    a = DoorTopSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.door_list.append(a)
                elif tile == 15:
                    a = CoinSprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.item_list.append(a)
                elif tile == 16:
                    a = KeySprite()
                    a.center_x = col_count * TILE_SIZE
                    a.center_y = row_count * TILE_SIZE
                    self.key_list.append(a)

                col_count += 1
            row_count -= 1

        self.player_sprite = PlayerSprite(hit_box_algorithm="Detailed")

        grid_x = 1
        grid_y = 1
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2

        # self.player_sprite.center_x = 600
        # self.player_sprite.center_y = 500

        self.player_list.append(self.player_sprite)

        damping = DEFAULT_DAMPING

        gravity = (0, -GRAVITY)

        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        def item_hit_handler(player_sprite, item_sprite, _arbiter, _space, _data):
            self.score_num += 10
            item_sprite.remove_from_sprite_lists()
            self.coin_music = arcade.play_sound(self.coin_music_file, 0.1, True, speed=0.7)

        self.physics_engine.add_collision_handler('player', "item", post_handler=item_hit_handler)

        def kill_hit_handler(player_sprite, spike_sprite, _arbiter, _space, _data):
            self.player_sprite.die()
            arcade.stop_sound(self.background_music)
            self.gameover_music = arcade.play_sound(self.gameover_music_file, 0.1, True, speed=0.7)
            self.game_end = True

        self.physics_engine.add_collision_handler('player', "kill", post_handler=kill_hit_handler)

        def door_hit_handler(player_sprite, spike_sprite, _arbiter, _space, _data):
            player_sprite.center_x = 500
            player_sprite.center_y = 500
            self.game_win = True
            if not self.have_key:
                self.draw_need_key = True

        self.physics_engine.add_collision_handler('player', "door", post_handler=door_hit_handler)

        def key_hit_handler(player_sprite, key_sprite, _arbiter, _space, _data):
            self.have_key = True
            key_sprite.remove_from_sprite_lists()
            self.coin_music = arcade.play_sound(self.coin_music_file, 0.1, True, speed=0.7)

        self.physics_engine.add_collision_handler('player', "key", post_handler=key_hit_handler)

        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.item_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="item")

        self.physics_engine.add_sprite_list(self.kill_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="kill")

        self.physics_engine.add_sprite_list(self.door_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="door")

        self.physics_engine.add_sprite_list(self.key_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="key")

    def setup(self):
        pass

    def on_key_press(self, key, modifiers):
        if self.player_sprite.dead:
            return
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.player_music = arcade.play_sound(self.player_music_file, 0.1, True, speed=0.7)
            self.up_pressed = True
            if self.physics_engine.is_on_ground(self.player_sprite):
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
        elif key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_update(self, delta_time):
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        if self.left_pressed and not self.right_pressed:
            if is_on_ground:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            if is_on_ground:
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)

        else:
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        self.physics_engine.step()

    def on_draw(self):
        self.clear()
        # arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        # for line in range(40):
        #     arcade.draw_line(0, line * TILE_SIZE, SCREEN_WIDTH, line * TILE_SIZE, arcade.color.BLACK)
        #     arcade.draw_line(line * TILE_SIZE, 0, line * TILE_SIZE, SCREEN_HEIGHT, arcade.color.BLACK)
        self.wall_list.draw()
        self.item_list.draw()
        self.kill_list.draw()
        self.door_list.draw()
        self.key_list.draw()
        self.player_list.draw()
        self.manager.draw()
        arcade.draw_text(f"Score: {int(self.score_num)}", 1000, 650, arcade.color.BLUE_GREEN, font_size=30)

        # Проигрыш
        if self.game_end:
            self.window.show_view(DiedView(self))

        # Требование ключа
        if self.draw_need_key:
            arcade.draw_text(f"You need key", self.player_sprite.center_x - 200, self.player_sprite.center_y - 50,
                             arcade.color.RED, font_size=30)
            self.draw_need_key = False
            self.game_win = False

        # Победа
        if self.game_win and self.have_key:
            arcade.stop_sound(self.background_music)
            self.win_sound = arcade.play_sound(self.win_sound_file, 0.1, speed=0.7)
            self.window.show_view(WinView(self))


class PauseView(arcade.View):
    def __init__(self, game: GameWindow):
        super().__init__()
        self.game = game
        self.background_image = arcade.load_texture('background.jpg')
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        # Кнопка resume
        resume_button = arcade.gui.UIFlatButton(text='Resume', width=300)
        self.v_box.add(resume_button.with_space_around(bottom=20))

        # Кнопка exit
        exit_button = arcade.gui.UIFlatButton(text='Menu', width=300)
        exit_button.on_click = self.exit_game
        self.v_box.add(exit_button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center_x',
                anchor_y='center_y',
                child=self.v_box
            )
        )

        # Нажатие на кнопку resume
        @resume_button.event('on_click')
        def resume_game(event):
            self.game.setup()
            self.game.background_music = arcade.play_sound(self.game.background_music_file, 0.05, True, speed=0.7)
            self.window.show_view(self.game)

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        self.manager.draw()

    # Нажатие на кнопку exit
    def exit_game(self, event):
        message_box = arcade.gui.UIMessageBox(width=400,
                                              height=400,
                                              message_text='Вы уверены, что хотите выйти?',
                                              callback=self.user_pressed,
                                              buttons=['Да', 'Нет'])
        self.manager.add(message_box)

    # Callback функция для кнопки exit
    def user_pressed(self, button_text):
        if button_text == 'Да':
            self.clear()
            game_view = StartView()
            self.window.show_view(game_view)
            self.manager.clear()
        elif button_text == 'Нет':
            pass


class DiedView(arcade.View):
    def __init__(self, game: GameWindow):
        super().__init__()
        self.game = game
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.background_image = arcade.load_texture('background_died.png')
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        lose_text = arcade.gui.UITextArea(text=f'WASTED',
                                          text_color=arcade.color.RED,
                                          font_size=50,
                                          width=300,
                                          height=60,
                                          x=10)
        self.v_box.add(lose_text.with_space_around(bottom=30))

        score_text = arcade.gui.UITextArea(text=f'You score - {self.game.score_num}',
                                           text_color=arcade.color.BLUE_GREEN,
                                           font_size=30,
                                           width=300,
                                           x=self.v_box.center_x,
                                           y=self.v_box.center_y)
        self.v_box.add(score_text.with_space_around(bottom=30))

        restart_button = arcade.gui.UIFlatButton(text='Restart', width=300)
        self.v_box.add(restart_button.with_space_around(bottom=20))

        # Кнопка exit
        exit_button = arcade.gui.UIFlatButton(text='Menu', width=300)
        self.v_box.add(exit_button.with_space_around(bottom=20))

        @exit_button.event('on_click')
        def exit_game(event):
            self.clear()
            game_view = StartView()
            self.window.show_view(game_view)
            self.manager.clear()

        @restart_button.event('on_click')
        def restart_game(event):
            self.clear()
            game_view = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            game_view.setup()
            self.window.show_view(game_view)
            self.manager.clear()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center_x',
                anchor_y='center_y',
                child=self.v_box
            )
        )

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        self.manager.draw()


class WinView(arcade.View):
    def __init__(self, game: GameWindow):
        super().__init__()
        self.game = game
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.background_image = arcade.load_texture('background_died.png')
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        lose_text = arcade.gui.UITextArea(text=f'YOU WIN',
                                          text_color=arcade.color.RED,
                                          font_size=50,
                                          width=300,
                                          height=60,
                                          x=10)
        self.v_box.add(lose_text.with_space_around(bottom=30))

        score_text = arcade.gui.UITextArea(text=f'You score - {self.game.score_num}',
                                           text_color=arcade.color.BLUE_GREEN,
                                           font_size=30,
                                           width=300,
                                           x=self.v_box.center_x,
                                           y=self.v_box.center_y)
        self.v_box.add(score_text.with_space_around(bottom=30))

        # Кнопка Restart
        restart_button = arcade.gui.UIFlatButton(text='Restart', width=300)
        self.v_box.add(restart_button.with_space_around(bottom=20))

        # Кнопка Next Level
        next_level_button = arcade.gui.UIFlatButton(text='Next Level', width=300)
        self.v_box.add(next_level_button.with_space_around(bottom=20))

        # Кнопка exit
        exit_button = arcade.gui.UIFlatButton(text='Menu', width=300)
        self.v_box.add(exit_button.with_space_around(bottom=20))

        @exit_button.event('on_click')
        def exit_game(event):
            self.clear()
            game_view = StartView()
            self.window.show_view(game_view)
            self.manager.clear()

        @restart_button.event('on_click')
        def restart_game(event):
            self.clear()
            game_view = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            game_view.setup()
            self.window.show_view(game_view)
            self.manager.clear()

        @next_level_button.event('on_click')
        def next_level_game(event):
            message_box = arcade.gui.UIMessageBox(width=400,
                                                  height=400,
                                                  message_text='Coming soon...',
                                                  buttons=['ОK'])
            self.manager.add(message_box)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center_x',
                anchor_y='center_y',
                child=self.v_box
            )
        )

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        self.manager.draw()


if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    first_gui = StartView()
    window.show_view(first_gui)
    arcade.run()
