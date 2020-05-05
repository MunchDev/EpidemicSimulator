from data_miner import plot_tally
from helper import clear
from helper import print_error as stderr
from json import load

population = None
try:
    with open("../cache/population.json") as f:
        population = json.load(f)
    if population == None or len(population) == 0:
        stderr("Unable to load population! Aborting...")
        input("Press Enter to continue..."
        raise RuntimeError("Unable to load population!")
except:
    exit(-1)
        
def main():
    welcome_options = [
        "Show country tally plot",
        "Show world tally plot",
    ]
    option = welcome_screen_option(welcome_options)
    return 0    

def welcome_screen_option(options):
    i = None
    while True:
        clear()
        print("Welcome to Epidemic Simulator -- Console version")
        print("What do you like to do? (-1 to exit)\n")
        for i, option in zip(range(len(options)), options):
            print("({0}) {1}".format(i + 1, option))
        i = input("Your option > ")
        if i == "-1":
            exit(0)
        if i.isdigit() and 0 < int(i) <= len(options):
            i = int(i)
            break
    clear()
    return i - 1
    
if __name__ == "__main__":
    main()
