from flask import Flask, render_template, request, make_response
 

app = Flask(__name__)
application = app



@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html'))
    if request.cookies.get('name') is None:
        response.set_cookie('name', 'qq')
    else:
        response.set_cookie('name', 'qq', expires=0)
    return response
@app.route('/form', methods=['GET','POST'])
def form():
    return render_template('form.html')
    
@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = None
    error_msg = None
    if request.method == 'POST':
        try:
            operand1 = float(request.form.get('operand1'))
            operand2 = float(request.form.get('operand2'))
            operation = request.form.get('operation')
            if operation == '+':
                result = operand1+operand2
            elif operation == '-':
                result = operand1-operand2
            elif operation == '/':
                result = operand1/operand2
            elif operation == '*':
                result = operand1*operand2
        except ValueError:
            error_msg = 'Вводите только числа'
        except ZeroDivisionError:
            error_msg = 'На ноль делить нельзя'





    response = make_response(render_template('calc.html', result=result, error_msg=error_msg))
    return response

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    input_class = ''
    result=None
    error_msg=None
    if request.method == 'POST':
        number = str(request.form.get('number'))
        temp = check(number)
        if temp == "Недопустимый ввод. Неверное количество цифр." or temp == "Недопустимый ввод. В номере телефона встречаются недопустимые символы.":
            error_msg = temp
            input_class = 'is-invalid'
        else:
            result=temp
            input_class='is-valid'
    response = make_response(render_template('phone.html', result=result, error_msg=error_msg, input_class=input_class))
    return response

def check(s):
    alph = [" ","(",")","-",".","+"]
    number = s
    for i in range(0,len(s)):
        if s[i] in alph:
            number = number.replace(s[i],'')
        elif s[i].isdigit()==1:
            pass
        else:
            return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
    if len(number)==10:
        number = f'''8-{number[0:3]}-{number[3:6]}-{number[6:8]}-{number[8:10]}'''
    elif len(number)==11:
        number = f'''8-{number[1:4]}-{number[4:7]}-{number[7:9]}-{number[9:11]}'''
    else:
        return "Недопустимый ввод. Неверное количество цифр."
    return number
