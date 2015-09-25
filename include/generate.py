import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print "Config file not specified. Use default."
        filename = 'config'

