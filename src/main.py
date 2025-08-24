from argparse import ArgumentParser

def main():
    argumentsparser = ArgumentParser()
    argumentsparser.add_argument("--modo", choices=["desktop"], required=True)
    arguments = argumentsparser.parse_args()

if __name__ == "__main__":
    main()