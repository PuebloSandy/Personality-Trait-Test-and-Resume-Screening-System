function password_show_hide1() {
    var x = document.getElementById("passwordw");
    var y = document.getElementById("passwords");
    var show_eyes = document.getElementById("show_eyes");
    var hide_eyes = document.getElementById("hide_eyes");
    hide_eyes.classList.remove("d-nones");
    if (x.type === "password" && y.type === "password") {
      x.type = "text";
      y.type = "text";
      show_eyes.style.display = "none";
      hide_eyes.style.display = "block";
    } else {
      x.type = "password";
      y.type = "password";
      show_eyes.style.display = "block";
      hide_eyes.style.display = "none";
    }
  }