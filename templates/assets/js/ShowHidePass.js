const togglePassword = document.querySelector(".togglePassword");
const password = document.querySelector(".passwordInput");

const toggleConfirmPassword = document.querySelector(".toggleConfirmPassword");
const confirmPassword = document.querySelector(".confirmPasswordInput");

const toggleLoginPassword = document.querySelector(".toggleLoginPassword");
const loginPassword = document.querySelector(".loginPasswordInput");



togglePassword.addEventListener("click", function (e) {
    console.log(e.target.previousElementSibling, "password")
    const type = e.target.previousElementSibling.getAttribute("type") === "password" ? "text" : "password";
    e.target.previousElementSibling.setAttribute("type", type);
    if (togglePassword.src.match("../assets/images/not_show_pass.png")) {
        togglePassword.src = "../assets/images/show_pass.png";
    } else {
        togglePassword.src = "../assets/images/not_show_pass.png";
    }
})


toggleConfirmPassword.addEventListener("click", function (e) {
    console.log(e.target.previousElementSibling, "confirmPassword")
    const type = e.target.previousElementSibling.getAttribute("type") === "password" ? "text" : "password";
    e.target.previousElementSibling.setAttribute("type", type);
    if (toggleConfirmPassword.src.match("../assets/images/not_show_pass.png")) {
        toggleConfirmPassword.src = "../assets/images/show_pass.png";
    }
    else {
        toggleConfirmPassword.src = "../assets/images/not_show_pass.png";
    }
})

toggleLoginPassword.addEventListener("click", function (e) {
    console.log(e.target.previousElementSibling, "loginPassword")
    const type = e.target.previousElementSibling.getAttribute("type") === "password" ? "text" : "password";
    e.target.previousElementSibling.setAttribute("type", type);
    if (toggleLoginPassword.src.match("../assets/images/not_show_pass.png")) {
        toggleLoginPassword.src = "../assets/images/show_pass.png";
    }
    else {
        toggleLoginPassword.src = "../assets/images/not_show_pass.png";
    }
})




