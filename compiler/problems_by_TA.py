from top import e
from parser import parse, ParseError

def problem_by_TA():
    # Problem statement: Write the multiplication table of 17 till 15 terms
    code = """
            def f(g){
                var x = 17;
                var y = 5;

                def s(){
                    return x  + y+ g();
                };

                return s;
            };

            def const42(){
                return 42;
            };

            def const84(){
                return 84;
            };

            var s1 = f(const42);
            var s2 = f(const84);
            print(s2());
            print(s1());
           """
    try:
        ast = parse(code)
        e(ast)
    except ParseError as pe:
        print("Parse Error:", pe)
    except Exception as ex:
        print("Error:", ex)

if __name__ == "__main__":
    problem_by_TA()
