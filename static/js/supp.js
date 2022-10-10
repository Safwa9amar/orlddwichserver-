let setSuppStatus = document.querySelectorAll("[set-suppstatus]");
// const socket = io(`https://${document.domain}:${location.port}/`);
setSuppStatus.forEach((el) => {
  try {
    let status = el.getAttribute("set-suppstatus");
    let id = el.id;
    if (status === "True") {
      el.setAttribute("checked", true);
    } else if (status === "False") {
      el.removeAttribute("checked");
    }

    el.addEventListener("change", () => {
      fetch(`http://${document.domain}:${location.port}/edit_sup_status`, {
        mode: "cors",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: id, status: el.checked }),
      });
      // socket.emit("getSuppdata", { id: id, status: el.checked });
    });
  } catch (err) {
    console.log("soceket : ", err);
  }
});
