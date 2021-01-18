document.addEventListener("DOMContentLoaded", () => {
    var replies = document.querySelectorAll(".fa-reply");
    replies.forEach(element => {
        element.addEventListener("click", reply)
    });
    replies = document.querySelectorAll(".fa-eye")
    replies.forEach(element => {
        element.addEventListener("click", show_replies)
    });
});

function create_reply(id, parent, author, date, message) {
    var selector = '[data-comment-id = ' + '"' + parent + '"' +']';
    var par = document.querySelector(selector);
    var layer;
    if (par.getAttribute('data-type') == 'comment') {
        layer = 1;
    }
    else {
        layer = 0;
    }
    var color;
    if (par.getAttribute('data-color') == 0 && par.getAttribute('data-type') == 'comment') {
        color = 1;
    }
    else {
        color = 0;
    }

    var element = document.createElement("div");
    var article = document.createElement('article');
    var header = document.createElement('header');
    var body = document.createElement('div');
    var footer = document.createElement('footer');
    var ul;
    var li;
    var i;

    element.setAttribute('class', 'post-item item item-inside');
    element.setAttribute('data-comment-id', id);
    element.setAttribute('data-type', 'comment');
    element.setAttribute('data-layer', layer);
    element.setAttribute('data-color', color);
    article.setAttribute('class', 'post');
    header.setAttribute('class', 'post-header');
    body.setAttribute('class', 'post-body');
    footer.setAttribute('class', 'post-footer');

    ul = document.createElement('ul');
    li = document.createElement('li');
    li.innerHTML = author;
    ul.appendChild(li);
    li = document.createElement('li');
    li.innerHTML = new Date(Date.parse(date));
    ul.appendChild(li);
    header.appendChild(ul);

    body.innerHTML = message;

    ul = document.createElement('ul');
    li = document.createElement('li');
    i = document.createElement('i');
    i.setAttribute('class', 'fas fa-reply');
    i.addEventListener('click', reply)
    li.appendChild(i);
    ul.appendChild(li);
    li = document.createElement('li');
    i = document.createElement('i');
    i.addEventListener('click', show_replies)
    i.setAttribute('class', 'fas fa-eye');
    li.appendChild(i);
    ul.appendChild(li);
    footer.appendChild(ul);

    article.appendChild(header);
    article.appendChild(body);
    article.appendChild(footer);

    element.appendChild(article);

    selector = '[data-comment-id = ' + '"' + id + '"' +']';

    var current = document.querySelector(selector);
    if (current !== null) {
        current.remove();
    }

    if (par.getAttribute('data-type') == 'comment') {
        par.appendChild(element);
    }
    else {
        document.querySelector("#main-body").appendChild(element);
    }
};

function show_replies(event) {
    var topic = document.querySelector("[data-type='topic']").getAttribute('data-topic-id');
    var comment = event.currentTarget.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute('data-comment-id');
    var request;
    try {
        request = new XMLHttpRequest();
    } catch (e) {
        alert("Nie je možné spojenie");
        return false;
    }

    request.open("GET", '/comments/' + topic + '/' + comment, true);
    request.setRequestHeader("Content-type", "x-www-form-urlencoded");
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    request.onreadystatechange = () => {
        if (request.readyState == 4 && request.status >= 200 && request.status < 400) {
            var comments = JSON.parse(request.responseText)['comments'];
            console.log(comments);
            comments.forEach(element => {
                create_reply(element['id'], element['parent'], element['author'], element['date'], element['message']);
            });
        }
        else {

        }
    };
    request.send();
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function create_form(element) {
    var input = document.createElement('textarea');
    input.setAttribute('rows', '1');
    element.append(input);
};

function send_reply(event) {
    

    var topic = document.querySelector("[data-type='topic']").getAttribute('data-topic-id');
    var footer = event.currentTarget.parentNode.parentNode.parentNode;
    var parent = footer.parentNode.parentNode.getAttribute('data-comment-id');
    var text_area = footer.querySelector("textarea");
    var value = text_area.value;
    var request;

    event.currentTarget.removeEventListener("click", send_reply);
    event.currentTarget.parentNode.nextElementSibling.style.display = 'initial';
    text_area.remove();

    if (!value || value.trim() == '') {
        alert('Nie je možné odoslať komentár bez textu!');
        event.currentTarget.addEventListener("click", reply);
        return false;
    }

    try {
        request = new XMLHttpRequest();
    } catch (e) {
        alert("Nie je možné spojenie");
        return false;
    }

    request.open("POST", "/reply", true);
    request.setRequestHeader("Content-type", "application/json");
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    request.onreadystatechange = () => {
        if(request.readyState == 4) {
            if (request.status >= 200 && request.status < 400) {
                var element = JSON.parse(request.responseText);
                console.log(element);
                create_reply(element['id'], element['parent'], element['author'], element['date'], element['message']);
            }
            else {
                alert('Pre pridanie komentára sa musite prihlásiť');
            }
        }
    }
    request.send(JSON.stringify({'message' : value, 'parent_id' : parent, 'topic' : topic}))
    event.currentTarget.addEventListener("click", reply);
}

function reply(event) {
    var footer = event.currentTarget.parentNode.parentNode.parentNode;
    event.currentTarget.removeEventListener("click", reply);
    event.currentTarget.parentNode.nextElementSibling.style.display = 'none';
    create_form(footer);
    event.currentTarget.addEventListener("click", send_reply);
};