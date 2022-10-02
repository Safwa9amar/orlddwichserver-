 window.addEventListener('DOMContentLoaded',()=>{

    let delBtn = document.querySelectorAll("[delete-data]");
    let del_id_tagret = document.getElementById("del_id_tagret");
    console.log(delBtn, del_id_tagret);
    delBtn.forEach((el) => {
      el.addEventListener("click", (e) => {
        let id = parseInt(el.getAttribute("delete-data"));
        let url = el.getAttribute('delete_url')
        let html = `
          <a class='btn' id='${id}' href='${url}''> Oui </a>
        `
        del_id_tagret.innerHTML = html
      });
    });
    })