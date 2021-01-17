document.addEventListener("DOMContentLoaded", () => {
    replies = document.querySelectorAll(".fa-reply");
    replies.forEach(element => {
        element.addEventListener("click", create_form)
    });
    replies = document.querySelectorAll(".fa-eye")
    replies.forEach(element => {
        element.addEventListener("click", show_replies)
    });
});
function show_replies(event) {
    elem = event.currentTarget.parentNode.parentNode
    var ajaxRequest;
    try {
        ajaxRequest = new XMLHttpRequest();
    } catch (e) {
        alert("Nie je možné spojenie");
        return false;
    }
    ajaxRequest.open("GET", "/comments/" + elem.getAttribute("id").split('-')[1], true);
    ajaxRequest.setRequestHeader("Content-type", "x-www-form-urlencoded");
    ajaxRequest.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    ajaxRequest.onreadystatechange = () => {
        
        if (ajaxRequest.readyState == 4 && ajaxRequest.status >= 200 && ajaxRequest.status < 400) {
            comments = JSON.parse(ajaxRequest.responseText)["comments"];
            comments.forEach(element => {
                div_main = document.createElement("div");
                div_main.setAttribute("class", "item item-inside");
                div_main.setAttribute("id", "post-" + element["id"]);
                div_mess = document.createElement("div");
                div_mess.innerHTML = element["message"];
                div_author = document.createElement("div");
                div_author.innerHTML = element["author"];
                div_fas = document.createElement("div");
                div_fa = document.createElement("div");
                i_fas = document.createElement("i");
                i_fas.setAttribute("class", "fas fa-reply");
                div_fas.appendChild(i_fas);
                div_main.appendChild(div_mess);
                div_main.appendChild(div_author);
                div_main.appendChild(div_fas);
                document.querySelector("#post-" + element["parent"]).appendChild(div_main);
                i_fas.addEventListener("click", create_form);
            });

        }
    }
    ajaxRequest.send();
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
function create_form(event) {
    event.currentTarget.style.display = "none";
    inp = document.createElement("INPUT");
    inp.setAttribute("type", "text");
    inp.classList.add("reply-text");
    but = document.createElement("INPUT");
    but.setAttribute("type", "submit");
    but.value = "Odpovedať";
    form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "reply");
    form.setAttribute("id", "post-form");
    form.appendChild(inp);
    form.appendChild(but);
    el = document.createElement("div");
    el.classList.add("item-inside");
    el.classList.add("reply-form");
    el.appendChild(form);
    event.currentTarget.parentNode.insertBefore(el, event.currentTarget.nextSibling);
    but.addEventListener("click", (event) => {
        event.preventDefault();
        reply(event.currentTarget.parentNode.parentNode.parentNode.parentNode);
    });
};
function reply(elem) {
    var ajaxRequest;
    try {
        ajaxRequest = new XMLHttpRequest();
    } catch (e) {
        alert("Nie je možné spojenie");
        return false;
    }
    ajaxRequest.open("POST", "/reply", true);
    ajaxRequest.setRequestHeader("Content-type", "application/json");
    ajaxRequest.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    ajaxRequest.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    ajaxRequest.onreadystatechange = () => {
        
        if (ajaxRequest.readyState == 4 && ajaxRequest.status >= 200 && ajaxRequest.status < 400) {
            data = JSON.parse(ajaxRequest.responseText);
            comment = JSON.parse(data["comment"]);
            fields = comment["fields"];
            div_main = document.createElement("div");
            div_main.setAttribute("class", "item item-inside");
            div_main.setAttribute("id", "post-" + comment["pk"]);
            div_mess = document.createElement("div");
            div_mess.innerHTML = fields["message"];
            div_author = document.createElement("div");
            div_author.innerHTML = data["author"];
            div_fas = document.createElement("div");
            div_fa = document.createElement("div");
            i_fas = document.createElement("i");
            i_fas.setAttribute("class", "fas fa-reply");
            div_fas.appendChild(i_fas);
            div_main.appendChild(div_mess);
            div_main.appendChild(div_author);
            div_main.appendChild(div_fas);
            elem.querySelector(".reply-form").remove();
            elem.querySelector(".fa-reply").style.display = "initial";
            elem.appendChild(div_main);
            i_fas.addEventListener("click", create_form);
        }
    }
    ajaxRequest.send(JSON.stringify({'message' : elem.querySelector(".reply-text").value, 'topic' : document.querySelector('[id^=topic-]').getAttribute("id")
    .split('-')[1], 'parent_id' : elem.getAttribute("id").split('-')[1]}));
};