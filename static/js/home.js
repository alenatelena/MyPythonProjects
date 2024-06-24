var questions = {};
var rawPrompt = '';

// Ответы пользователя передаем на сервер для создания финального промпта
function compilePrompt() {
    fetch('/compile', {
        method: 'POST',
        body: JSON.stringify({ questions }),
        headers: {
            'X-auth-user': localStorage.getItem('user')
        }
    }
    ).then(
        response => response.json()
    ).then(data => {
        var prompt = data;
        var text = document.createElement('p');
        text.innerText = prompt;
        text.className += "regular-text";
        text.id = 'finalPrompt';
        document.getElementById('serverText').appendChild(text);
        document.getElementById('serverText').removeChild(document.getElementById('compileBtn'));
        questions = {};
    })
}

// Отвечает за очистку предыдущего вопроса и показ нового 
function nextQuestion(params) {
    var inpId = this.id.split('-').at(0);
    var inp = document.getElementById(inpId);
    var lbl = document.getElementById(inpId + '-label');
    document.getElementById('serverText').removeChild(inp);
    document.getElementById('serverText').removeChild(lbl);
    document.getElementById('serverText').removeChild(this);

    questions[inpId].answer = inp.value;

    if (questions[Number(inpId) + 1]) {
        var inp2 = document.getElementById(String(Number(inpId) + 1));
        var lbl2 = document.getElementById(String(Number(inpId) + 1) + '-label');
        var btn2 = document.getElementById(String(Number(inpId) + 1) + '-btn');

        inp2.style = 'width: 300px;';
        lbl2.style = '';
        btn2.style = 'width: 150px;';
    } else {
        var confirm = document.createElement('button');
        confirm.id = 'compileBtn';
        confirm.onclick = compilePrompt;
        confirm.innerText = 'Сформировать промпт';
        confirm.classList.add("button");
        confirm.style = 'width: 200px';
        document.getElementById('serverText').appendChild(confirm);
    }
}

// Отображаем ворпос для пользователя
// Создается элемент с текстом вопроса, поле для ввода ответа, кнопка сохранения ответа
function drawQuestions(question, index) {
    // Записываем ответ в объект типа "вопрос: ответ"
    questions[index] = {
        label: question,
    };

    // Создаем поле ввода и добавляем к нему стили
    var inp = document.createElement('input');
    inp.id = String(index);
    var inpStyle = 'width: 300px;';
    inp.style = index === 0 ? inpStyle : inpStyle + ' position: absolute; display: none';
    inp.setAttribute("class", "question-input")
    // inp.className += "question-input";

    // Создаем текст вопроса и добавляем к нему стили
    var lb = document.createElement('label');
    lb.innerText = question;
    lb.id = String(index) + '-label';
    lb.style = index !== 0 && 'position: absolute; display: none';
    lb.setAttribute("class", "regular-text");
    // lb.classList.add("regular-text");

    // Создаем кнопку и добавляем к ней стили
    var btn = document.createElement('button');
    btn.innerText = 'Сохранить';
    btn.id = String(index) + '-btn';
    // btn.classList.add("button");
    btn.setAttribute("class", "button");

    // Также добавляем функцию, которая срабатывает на нажатие кнопки
    btn.onclick = nextQuestion;
    var btnStyle = 'width: 150px;';
    btn.style = index === 0 ? btnStyle : btnStyle + 'position: absolute; display: none';

    // В элемент serverText кладем созданные элементы
    document.getElementById('serverText').appendChild(lb);
    document.getElementById('serverText').appendChild(inp);
    document.getElementById('serverText').appendChild(btn);
}

// Функция для отправки запроса на сервер и обновления содержимого HTML страницы
function fetchData() {
    if (document.getElementById('finalPrompt')) document.getElementById('serverText').removeChild(document.getElementById('finalPrompt'));

    var textField = document.getElementById("textInput");
    var textValue = textField.value;
    fetch('/', {
        method: 'POST',
        body: JSON.stringify({ // Преобразование данных в формат JSON
            textInput: textValue
        }),
        headers: {
            'X-auth-user': localStorage.getItem('user')
        }
    })
        .then(response => response.json())  // Преобразуем ответ сервера в JSON
        .then(data => {
            // Обновляем содержимое элемента с id="serverText" полученными данными
            var questions = JSON.parse(data);
            rawPrompt = questions;
            // Отрисовываем все вопросы
            questions.forEach(drawQuestions);
        })
        .catch(error => console.error('Ошибка при получении данных с сервера:', error));
}

function clearText() {
    questions = {}
    document.getElementById("serverText").outerHTML = "";
    // document.body.removeChild(div);
    var newText = document.createElement("div");
    newText.className = "serverText";
    newText.id = "serverText";
    document.getElementById("main").appendChild(newText);
}

function toLogin() {
    window.location.href = '/login'
}

function logout() {
    localStorage.removeItem('user')
    window.location.href = '/'
}