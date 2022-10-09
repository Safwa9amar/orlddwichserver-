let setSuppStatus = document.querySelectorAll("[set-suppstatus]");
const socket = io(`https://${document.domain}:${location.port}/`);
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
      socket.emit("getSuppdata", { id: id, status: el.checked });
    });
  } catch (err) {
    console.log("soceket : ", err);
  }
});
