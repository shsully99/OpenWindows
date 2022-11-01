// Get the button that opens the modal
let btnRegistration = document.querySelectorAll(".myBtnRegistration");
// console.log(btnRegistration)
let modalRegistration = document.getElementById("myModalRegistration");

let btnLogIn = document.querySelectorAll(".myBtnLogIn");
let modalLogIn = document.getElementById("myModalLogIn");

let btnForgetPass = document.querySelectorAll(".myBtnForgetPass");
let modalForgetPass = document.getElementById("myModalForgetPass");

let btnCheckEmail = document.querySelectorAll(".myBtnCheckEmail");
let modalCheckEmail = document.getElementById("myModalCheckEmail");


let btnShare=document.querySelectorAll(".myBtnShare")
// console.log(btnShare)
let modalShare=document.getElementById("myModalShare")
let spanShare = document.getElementsByClassName("close_share_modal")[0];



function closeAllModals (){
    let modals = document.querySelectorAll(".modal");

    modals.forEach((item,index)=>{
        item.style.display = "none"
    })
}
// Get the <span> element that closes the modal
// let span = document.getElementsByClassName("close_modal")[0];

// When the user clicks the button, open the modal
for (let i = 0; i < btnRegistration.length; i++) {
    btnRegistration[i].addEventListener("click", function () {
        closeAllModals()
        modalRegistration.style.display = "block";
    })
}
for (let i = 0; i < btnLogIn.length; i++) {
    btnLogIn[i].addEventListener("click", function () {
        closeAllModals()
        modalLogIn.style.display = "block";
    })
}

for (let i = 0; i < btnForgetPass.length; i++) {
    btnForgetPass[i].addEventListener("click", function () {
        closeAllModals()
        console.log(modalShare,"gfhtrh")

        modalForgetPass.style.display = "block";
    })
}

for (let i = 0; i < btnShare.length; i++) {
    btnShare[i].addEventListener("click", function () {
        closeAllModals()
        console.log(modalShare,"gfhtrh")

        modalShare.style.display = "block";
    })
}

for (let i = 0; i < btnCheckEmail.length; i++) {
    btnCheckEmail[i].addEventListener("click", function () {
        closeAllModals()
        console.log(modalCheckEmail,"gfhtrh")

        modalCheckEmail.style.display = "block";
    })
}

window.onclick = function (event) {
    if (event.target === modalRegistration) {
        modalRegistration.style.display = "none";
    }
    if (event.target === modalLogIn) {
        modalLogIn.style.display = "none";
    }
    if (event.target === modalForgetPass) {
        console.log(modalForgetPass,"gfhtrh")
        modalForgetPass.style.display = "none";
    }
    if (event.target === modalCheckEmail) {
        console.log(modalCheckEmail,"gfhtrh")
        modalCheckEmail.style.display = "none";
    }

    if (event.target === modalShare) {
        console.log(modalShare,"gfhtrh")
        modalShare.style.display = "none";
    }


    // When the user clicks on <span> (x), close the modal
    spanShare.onclick = function() {
        modalShare.style.display = "none";
    }

}
