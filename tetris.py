# TODO
# Add completed row removal and score
# add shapes
# add next shape box
# add hold key operation    

# DONE
# fix soundtrack
# add music(on/off) button

import arcade
import pathlib

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Tetris"
path = pathlib.Path(__file__).parent
imagepath = path / "images"
soundpath = path / "sound"

START_X = 220
START_Y = 700

# Score variables
collision_increment = 5
# row_increment = 100 # Currently unused

class MyGame(arcade.Window):
    # Main class
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.sprite = None
        self.music = None
        self.bottom_row = []
        self.endgame = None
        self.score = None
        self.mute = None

    def setup(self):
        self.endgame = False
        self.score = 0
        self.mute = 1
        self.music = arcade.Sound(str(soundpath.absolute() / "music.wav"), streaming=True)
        self.music.play(0.5)
        self.sprite = arcade.Sprite(imagepath / "blue.png", center_x=START_X, center_y=START_Y)
        for i in range(20):
            self.bottom_row.append(arcade.Sprite(imagepath / "blue.png", center_x=20 + i*50, center_y=20))

    def on_draw(self):
        arcade.start_render()
        self.sprite.draw()
        for box in self.bottom_row:
            box.draw()
        
        # draw score
        arcade.draw_text(f"Score = {self.score}", start_x= 20, start_y=START_Y+50, color = arcade.color.WARM_BLACK, font_size=24)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            if self.sprite.center_x < 50:
                pass
            else:
                self.sprite.center_x = self.sprite.center_x - 50
            for box in self.bottom_row:
                if self.sprite and arcade.check_for_collision(self.sprite, box):
                    self.sprite.center_x = self.sprite.center_x + 50

        if key == arcade.key.RIGHT:
            if self.sprite.center_x > SCREEN_WIDTH - 50:
                pass
            else:
                self.sprite.center_x = self.sprite.center_x + 50
            for box in self.bottom_row:
                if self.sprite and arcade.check_for_collision(self.sprite, box):
                    self.sprite.center_x = self.sprite.center_x - 50

        if key == arcade.key.DOWN:
            self.sprite.change_y = - 25

        if key == arcade.key.M:
            # Toggle mute
            if not self.mute %2 == 0:
                self.music.stop()
                self.mute = self.mute + 1 
            else:
                self.music.play(0.5)
                self.mute = self.mute + 1


    def on_update(self, delta_time: float):
        if self.endgame:
            return

        self.sprite.update() # Enables sprite.change_y to update

        distance = 2
        self.sprite.center_y = self.sprite.center_y - distance

# Check for collision   
        collision = False
        for box in self.bottom_row:
            if self.sprite and arcade.check_for_collision(self.sprite, box):
                collision = True
                break
        
        if collision:
            self.score = self.score + collision_increment
            self.bottom_row.append(self.sprite)
            self.sprite.center_y = box.center_y + 50
            if self.sprite.center_y > START_Y:
                self.endgame = True
            else:
                self.sprite = arcade.Sprite(imagepath / "blue.png", center_x=START_X, center_y=START_Y)

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()