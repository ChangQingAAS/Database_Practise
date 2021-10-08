import argparse
from init import init
from reset import reset

def before_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("e",
                        nargs='?',
                        const=" ",
                        help="whether init or reset the database")
    args = parser.parse_args()
    if args.e == "init":
        init()
    elif args.e == "reset":
        reset()
    elif args.e == "help":
        print("init your database before run, please enter: python main.py init")
        print("reset your database before run, please enter: python main.py reset")
    else:
        # print("there is no ", args.e)
        pass