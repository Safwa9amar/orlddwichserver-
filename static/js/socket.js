document.addEventListener("DOMContentLoaded", () => {
  const socket = io(`https://${document.domain}:${location.port}/`);

  try {
    let notification_indicator = document.getElementById(
      "notification_indicator"
    );
    let notification_area = document.getElementById("notification_area");
  } catch (error) {}

  socket.emit("message", { test: "server side connected from socket file" });

  socket.on("message", function (data) {
    try {
      notification_indicator.textContent = JSON.parse(data).length;
      let html = `
      <a href="#" class="flex gap-4 items-stratch">
        <div class="avatar">
          <div class="w-10 rounded-full">
            <img src="https://placeimg.com/192/192/people" />
          </div>
        </div>
        <div class="flex flex-col gap-2">
          <h1>john doe a passé une commande</h1>
          <p>29 July 2020 - 02:26 PM</p>
        </div>
      </a>
      `;
      notification_area.innerHTML = html;
    } catch (error) {}
  });
});
