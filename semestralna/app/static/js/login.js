document.addEventListener("DOMContentLoaded", () => {
    error_list = document.querySelectorAll(".error");
    for (let index = 0; index < error_list.length; index++) {
        error_list[index].addEventListener('keyup', (event) => {
            event.currentTarget.classList.remove("error");
            event.currentTarget.querySelector(".help-block").remove();
        }, {once: true})
    }
})