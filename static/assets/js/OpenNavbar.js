
    function openNav() {
    console.log("click")
    let x = document.getElementById("links");
    if (x.style.display === "block") {
    x.style.display = "none";
} else {
    x.style.display = "block";
}
}