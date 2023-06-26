let create = document.querySelector("#create");
let close = document.querySelector("#close");
let update = document.querySelector("#update");
let modal = document.querySelector("#formato");
let Umodal = document.querySelector("#update");
let submit = document.querySelector("#submitBtn");

create.addEventListener("click", () => {
    modal.style.display = "flex";
});

update.addEventListener("click", () => {
  Umodal.style.display = "flex";
});

close.addEventListener("click", () => {
  modal.style.display = "none";
  Umodal.style.display = "none";
})
submit.addEventListener("click", () => {
   modal.style.display = "none";
})

  

  /*let vista_preliminar = (event) => {
    let leer_img = new FileReader();
    let id_img = document.getElementById("img-foto");

    leer_img.onload = () => {
      if (leer_img.readyState == 2) {
        id_img.src = leer_img.result;
        id_img.style.display = "block";
      }
    };

    leer_img.readAsDataURL(event.target.files[0]);
  };*/
  

  window.onload = function () {
    document.getElementById("password1").onchange = validatePassword;
    document.getElementById("password2").onchange = validatePassword;
  };

  function validatePassword() {
    var pass2 = document.getElementById("password2").value;
    var pass1 = document.getElementById("password1").value;
    if (pass1 != pass2)
      document
        .getElementById("password2")
        .setCustomValidity("Las contraseñas no coinciden!!");
    else document.getElementById("password2").setCustomValidity("");
    //empty string means no validation error
  }


