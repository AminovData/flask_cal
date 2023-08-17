from venv import create
from flask import Flask, render_template, abort, request
import re



## math functions
def plus_num(val1,val2):
    x =  float(val1)
    y =  float(val2)
    result = x + y
    return str(result)

def minus_num(val1,val2):
    x =  float(val1)
    y =  float(val2)
    result = x - y
    return str(result)

def mul_num(val1,val2):
    x =  float(val1)
    y =  float(val2)
    result = x * y
    return str(result)

def divide_num(val1,val2):
    x =  float(val1)
    y =  float(val2)
    result = x / y
    return str(result)

def percent(problem):
    percent = float(problem) / 100
    return percent



def operation_menu(val1, val2, operation):
    if operation == "+":
            return plus_num(val1, val2)
    elif operation == "-":
            return minus_num(val1, val2)
    elif operation == "*":
            return mul_num(val1, val2)
    elif operation == "/":
            return divide_num(val1, val2)
    else:
        print("Вы выбрали не правильную опцию...")#


def operation_count(problem):
    
    if problem[0] == "-":
        problem = problem[1:]
    
    patern = r"[\+|\-|\*|\/]"
    operations = re.findall(patern, problem)
    devide_oper = [symbol for symbol in operations if symbol == "/"]
    multiply_oper = [symbol for symbol in operations if symbol == "*"]
    minus_oper = [symbol for symbol in operations if symbol == "-"]
    plus_oper = [symbol for symbol in operations if symbol == "+"]

    operations = [devide_oper,multiply_oper,minus_oper,plus_oper]

    
    return operations



def problem_handler(problem=None,mode=None,):
    
    if mode == "usuall_math":
        operation_oder = ["/","*","-","+"]
        operations = operation_count(problem)
        
        
        for operation,symbol in zip(operations, operation_oder):
            print(problem)
            for op in operation:
                while operation:
                    patern = fr"-?[\d.]+\{symbol}[\d.]+"
                    find_problem = re.search(patern,problem)
                    print(symbol)
                    problem_str = find_problem.group()
                    if symbol == "-":
                        if problem_str[0] == "-" and len(problem_str.split(f"-")) == 3:
                            inus_val,val1,val2 = problem_str.split(f"-")
                            val1 = "-" + val1
                        elif len(problem_str.split("-")) == 4:
                            minus_1,val_1,minus_2,val_2 = problem_str.split("-")
                            val1 = "-" + val_1
                            val2 = "-" + val_2
                        else:
                            val1,val2 = problem_str.split(f"-")
                    else:
                        val1,val2 = problem_str.split(f"{symbol}")
                   # print(symbol)
                    result = operation_menu(val1,val2, operation=symbol)
                    problem  = problem.replace(problem_str, result)
                    operation.pop(0)
        return result
    elif mode == "percent":
        return percent(problem)
        
    



# @app.route("/")
# def home():
#     return render_template("home.html")

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def home():
        if request.method == 'GET':
            return render_template("home.html")
        elif request.method == 'POST':
            problem_data = request.form["data_to_cal"] 
            pattern = "-?[\d.]+[\/|\*|\+|\-][\d.]"
            match = re.search(pattern,problem_data)
            if match:
                result_data = problem_handler(problem_data,"usuall_math")
                return render_template("home.html", result_data = result_data)
            elif "%" in problem_data:
                problem_data = problem_data.replace("%", "")
                result_data = problem_handler(problem_data,"percent")
                return render_template("home.html", result_data = result_data)
            else:
                return render_template("home.html", result_data = problem_data)
        else:
            problem_data = request.form["data_to_cal"]
            
        return app

if __name__ == '__main__':
     app.debug = True
     app.run()
