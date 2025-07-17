import subprocess
from PIL import Image

DEFAULT_SCREENSHOT_FILEPATH = "./screen.png"

class IntVector2:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __add__(self, other:'IntVector2') -> 'IntVector2':
        
        x = self.x + other.x
        y = self.y + other.y

        return IntVector2(x,y)

    def __sub__(self, other:'IntVector2') -> 'IntVector2':
        x = self.x - other.x
        y = self.y - other.y

        return IntVector2(x,y)

    def __iter__(self):
        yield self.x
        yield self.y
    
    def __repr__(self):
        return f"IntVector2(x={self.x}, y={self.y})"

    def __eq__(self, other:object) -> bool:
        if not isinstance(other, IntVector2):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def To_Tuple_XY(self):
        return (self.x, self.y)
    
    def To_Tuple_YX(self):
        return (self.y, self.x)

class Boundaries:
    def __init__(self, top_left:IntVector2, bottom_right:IntVector2):
        self.top_left = top_left
        self._bottom_right = bottom_right
    
    def Get_Dimensions(self) -> IntVector2:
        return self._bottom_right - self.top_left

def tap(coords:IntVector2) -> None:
    subprocess.run(f"adb shell input tap {coords.x} {coords.y}", shell=True)

def take_screenshot(fp:str=DEFAULT_SCREENSHOT_FILEPATH) -> None:
    subprocess.run(f"adb exec-out screencap -p > {fp}", shell=True)

def get_screen_resolution() -> IntVector2:
    output = subprocess.check_output(f"adb shell wm size", shell=True, text=True).strip()
    x,y = output[15:].split("x")

    return IntVector2(int(x),int(y))

def get_grid_boundaries(image:Image.Image) -> Boundaries:
    FLOW_FREE_GRID_BORDER_COLOUR = (127,63,63)
    screen_width, screen_height = get_screen_resolution()
    
    top_left_found_coord = IntVector2(0,0)
    bottom_right_found_coord = IntVector2(0,0)

    is_top_left_pixel_found = False
    is_bottom_right_pixel_found = False

    for y in range(screen_height):
        for x in range(screen_width):
            top_left_coord = IntVector2(x,y)
            bottom_right_coord = IntVector2(screen_width-1-x, screen_height-1-y) 

            top_left_pixel = image.getpixel(top_left_coord.To_Tuple_XY())
            bottom_right_pixel = image.getpixel(bottom_right_coord.To_Tuple_XY())

            if not is_top_left_pixel_found and top_left_pixel == FLOW_FREE_GRID_BORDER_COLOUR:
                top_left_found_coord = top_left_coord
                is_top_left_pixel_found = True
            
            if not is_bottom_right_pixel_found and bottom_right_pixel == FLOW_FREE_GRID_BORDER_COLOUR:
                bottom_right_found_coord = bottom_right_coord
                is_bottom_right_pixel_found = True

            if is_top_left_pixel_found and is_bottom_right_pixel_found: break

        if is_top_left_pixel_found and is_bottom_right_pixel_found: break

    
    if not is_top_left_pixel_found:
        raise(Exception("Could not find top left corner of the Flow Free grid on the screen. Make sure screen is on a Flow Free level."))
    
    if not is_bottom_right_pixel_found:
        raise(Exception("Could not find bottom right corner of the Flow Free grid on the screen. Make sure screen is on a Flow Free level."))

    grid_boundaries = Boundaries(top_left_found_coord, bottom_right_found_coord)
    return grid_boundaries

def get_board(grid_boundaries:Boundaries):
    pass
    
    
def main():
    take_screenshot()
    image = Image.open(DEFAULT_SCREENSHOT_FILEPATH).convert("RGB")
    grid_boundaries = get_grid_boundaries(image)
    print(grid_boundaries)
    


if __name__ == "__main__":
    main()
