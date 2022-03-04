from shifty_face import ShiftyFace

if __name__ == "__main__":
    sf = ShiftyFace(100, settings={"assets_directory": "substrapunks"})

    sf.generate()