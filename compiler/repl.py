from parser import parse, ParseError
from top import e, Environment

def main():
    env = Environment()
    print("Enter 'exit' to quit.")
    while True:
        try:
            line = input(">>> ")
            if line.strip().lower() == "exit":
                break
            if not line.strip():
                continue
            tree = parse(line)
            result = e(tree, env)
            if line.strip().endswith(";"):
                pass  # Do not print the result
            else:
                if result is not None:
                    print(result)
        except ParseError as pe:
            print("Parse Error:", pe)
        except Exception as ex:
            print("Error:", ex)

if __name__ == "__main__":
    main()
