from colorama import Fore
from query import query


def start():
    instructions=(
        "Welcome to the LangChain QA System! You can ask questions about LangChain, and I'll provide answers based on the loaded documents."
    )
    print(Fore.BLUE + "\n\x1B[3m" + instructions + "\x1B[0m" + Fore.RESET)

    print("MENU")
    print("====")
    print("[1]- Ask a question")
    print("[2]- Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        ask()
    elif choice == "2":
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice")
        start()


def ask():
    while True:
        user_input = input("Q: ")
        # Exit
        if user_input == "x":
            start()
        else:
            response = query(user_input)
            print(Fore.BLUE + "===== FINAL ANSWER: =====" + Fore.RESET)
            print(Fore.WHITE + response + Fore.RESET)
            print("\n-------------------------------------------------")


if __name__ == "__main__":
    start()
