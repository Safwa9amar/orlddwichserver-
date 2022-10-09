document.addEventListener("DOMContentLoaded", () => {
  try {
    let multipleSelection = document.getElementById("multipleSelection");
    let added_categories = document.getElementById("added_categories");
    let arr = [];
    multipleSelection.addEventListener("keyup", (e) => {
      let target = e.target;
      let text = target.value;
      let index = arr.indexOf(text);

      let span = document.createElement("span");
      span.classList.add("badge");
      span.classList.add("badge-primary");
      span.classList.add("cursor-pointer");
      span.classList.add("hover:text-red-400");

      span.addEventListener("click", (e) => {
        let deletd_txt = e.target.textContent;
        let index = arr.indexOf(deletd_txt);
        if (index != -1) {
          arr.splice(index, 1);
        }
        e.target.remove();
        console.log(arr);
      });
      target.value = "";
      if (index !== -1) return;
      if (text === "") return;
      span.textContent = text;
      arr.push(text);
      let i = document.createElement("i");
      i.classList.add("fa-solid");
      i.classList.add("fa-trash");
      i.classList.add("mx-2");
      i.classList.add("pointer-events-none");
      i.classList.add("hover:text-red-400");
      span.appendChild(i);
      added_categories.appendChild(span);
    });
    document
      .getElementById("submitAddingSupp")
      .addEventListener("click", (e) => {
        multipleSelection.value = arr.toString();
      });
  } catch (error) {}
});
