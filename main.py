from modules.window import Window
import logging
import settings
logging.basicConfig(level=logging.INFO)



def main():
    bls = Window("Blue")
    bls.set_size_window()


if __name__ == "__main__":
    main()
