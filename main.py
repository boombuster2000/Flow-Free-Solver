import subprocess
from PIL import Image

def tap(x:int, y:int) -> None:
    subprocess.run(f"adb shell input tap {x} {y}", shell=True)

def take_screenshot(fp:str="screen") -> None:
    subprocess.run(f"adb exec-out screencap -p > {fp}.png", shell=True)

def get_screen_resolution() -> tuple[int,int]:
    output = subprocess.check_output(f"adb shell wm size", shell=True, text=True).strip()
    x,y = output[15:].split("x")
    return (int(x), int(y))

def get_grid_boundaries(image: Image.Image) -> dict[str, tuple[int, int]]:
    FLOW_FREE_GRID_BORDER_COLOUR = (127,63,63)
    screen_width, screen_height = get_screen_resolution()

    grid_boundaries = {
        "top-left": (0,0),
        "bottom-right": (screen_width, screen_height)
    }

    is_top_left_pixel_found = False
    is_bottom_right_pixel_found = False

    for y in range(screen_height):
        for x in range(screen_width):
            top_left_coord = (x,y)
            bottom_right_coord = (screen_width-1-x, screen_height-1-y) 

            top_left_pixel = image.getpixel(top_left_coord)
            bottom_right_pixel = image.getpixel(bottom_right_coord)

            if not is_top_left_pixel_found and top_left_pixel == FLOW_FREE_GRID_BORDER_COLOUR:
                grid_boundaries["top-left"] = top_left_coord
                is_top_left_pixel_found = True
            
            if not is_bottom_right_pixel_found and bottom_right_pixel == FLOW_FREE_GRID_BORDER_COLOUR:
                grid_boundaries["bottom-right"] = bottom_right_coord
                is_bottom_right_pixel_found = True

            if is_top_left_pixel_found and is_bottom_right_pixel_found: break

        if is_top_left_pixel_found and is_bottom_right_pixel_found: break

    
    if not is_top_left_pixel_found:
        raise(Exception("Could not find top left corner of the Flow Free grid on the screen. Make sure screen is on a Flow Free level."))
    
    if not is_bottom_right_pixel_found:
        raise(Exception("Could not find bottom right corner of the Flow Free grid on the screen. Make sure screen is on a Flow Free level."))


    return grid_boundaries

def get_board(screenshot_filepath : str): 
    image = Image.open(screenshot_filepath).convert("RGB")
    grid_boundaries = get_grid_boundaries(image)

    print(grid_boundaries)
    
    
take_screenshot()
get_board("screen.png")
    



