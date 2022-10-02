window.addEventListener("DOMContentLoaded", () => {
  console.log("document loaded");
  let delBtn = document.querySelectorAll("[delete-data]");
  let del_id_tagret = document.getElementById("del_id_tagret");

  delBtn.forEach((el) => {
    el.addEventListener("click", (e) => {
      let id = parseInt(el.getAttribute("delete-data"));
      let url = el.getAttribute("delete_url");
      let html = `
          <a class='btn' id='${id}' href='${url}''> Oui </a>
        `;
      del_id_tagret.innerHTML = html;
    });
  });

  try {
    let = update_category_img = document.getElementById("update_category_img");
    update_category_img.addEventListener("change", (e) => {
      readURL(e, "categoryuploadImg");
    });

    let update_category_icon = document.getElementById("update_category_icon");
    update_category_icon.addEventListener("change", (e) => {
      readURL(e, "categoryuploadIcon");
    });
  } catch (e) {}

  try {
    // update_article_img = document.getElementById("uploadImg");
    update_article_img_input = document.getElementById("photo");
    update_article_img_input.addEventListener("change", (e) => {
      readURL(e, "uploadImg");
    });
  } catch (error) {}

  const readURL = (input, tagret_img_id) => {
    img = document.getElementById(tagret_img_id);

    let file_input = input.target.files;
    console.log(file_input);
    if (file_input && file_input[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        img.setAttribute("src", e.target.result);
      };

      reader.readAsDataURL(file_input[0]);
    }
  };

  let theme_toggle = document.getElementById("theme-toggle");
  let data_theme = document.querySelector("[data-theme]");
  localStorage.getItem("theme") == null && localStorage.setItem("theme", "dracula");

  data_theme.setAttribute("data-theme", localStorage.getItem("theme"));


  let moon = document.getElementById("moon");
  let sun = document.getElementById("sun");  
  let theme = localStorage.getItem("theme");

  if (theme === "garden") {
    moon.classList.replace("swap-on", "swap-off");
    sun.classList.replace("swap-off", "swap-on");
  } else {
    moon.classList.replace("swap-off", "swap-on");
    sun.classList.replace("swap-on", "swap-off");
  }
    theme_toggle.addEventListener("click", () => {
      console.log(data_theme.getAttribute("data-theme"));

      if (data_theme.getAttribute("data-theme") === "garden") {
        data_theme.setAttribute("data-theme", "dracula");
        localStorage.setItem("theme", "dracula");
      } else if (data_theme.getAttribute("data-theme") === "dracula") {
        data_theme.setAttribute("data-theme", "garden");
        localStorage.setItem("theme", "garden");
      }
    });
});
