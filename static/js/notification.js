document.addEventListener("DOMContentLoaded", () => {
  // const socket = io(`http://${document.domain}:${location.port}/test`);
  const url = `https://${document.domain}:${location.port}`;

  let fetshNotif = async () => {
    let res = await fetch(`${url}/notifications`, {
      mode: "cors",
      method: "GET",
    }).then((res) => res.json());

    return res;
  };
  try {
    let notification_indicator = document.getElementById(
      "notification_indicator"
    );

    // let notification_area = document.getElementById("notification_area");
    let notif_indicator = document.getElementById("notif_indicator");
  } catch (error) {}

  // socket.emit("message", {
  //   test: "server side connected from socket file",
  // });

  // socket.on("connect", function (data) {
  //   console.log("connected");
  // });
  // socket.on("order", function (data) {
  // console.log("msg from server");
  setInterval(() => {
    fetshNotif()
      .then((data) => {
        let newData = data.filter((el) => el.isViewed !== true);
        // console.log(newData);
        notification_indicator.innerText = newData.length;
        if (newData.length <= 0) notification_indicator.style.display = "none";
        if (newData.length > 0) notification_indicator.style.display = "block";
        return data;
      })
      .then((data) => {
        notif_indicator.addEventListener("click", () => {
          // clearInterval(fetshNotification);

          let newViwedData = data.map((el) => el.id);
          fetch(`${url}/notifications`, {
            mode: "cors",
            method: "POST",
            headers: {
              "content-type": "application/json",
            },
            body: JSON.stringify({ viwedArr: newViwedData }),
          });
        });
        let newData = data.filter((el) => el.isReaded !== true);
        if (newData.length === 0) return;
        notification_area.innerHTML = "";
        try {
          document.getElementById("recent").innerHTML = "";
        } catch (error) {}

        newData.forEach((el) => {
          let html = `
        <a href="${url}/orders?order=${el.order_id}" class="w-full flex flex-col gap-2   " data-attr="${el.id}" >
            <h1>${el.custumer_nom} ${el.custumer_prenom} a passé une commande</h1>
            <p>${el.order_date}</p>
        </a>
        `;

          let span = document.createElement("span");
          span.innerHTML = html;
          notification_area.appendChild(span);

          // last camnnd appending

          let template = `
          <div class="w-full self-start flex items-start gap-4 justify-between">
            <div class="flex gap-2">
              <div class="w-32">
                <p>${el.custumer_nom} ${el.custumer_prenom}.</p>
                <a href="${url}/orders?order=${
            el.order.id
          }" class="text-warning font-bold">#${el.order.id}</a>
              </div>
            </div>
          <div class="flex gap-1">
                  <p class="font-bold">${el.order_date}</p>
                </div>
            <div class="flex items-center">
            ${
              (el.order.status === 2 &&
                '<button class="btn btn-xs btn-outline btn-info">Approuvé</button>') ||
              (el.order.status === 3 &&
                '<button class="btn btn-xs btn-outline btn-success">livré</button>') ||
              (el.order.status === 4 &&
                '<button class="btn btn-xs btn-outline btn-btn-ghost">annulé</button>') ||
              (el.order.status === 1 &&
                '<div class="btn btn-xs btn-outline btn-warning">en attendant</div>')
            }
           
             <div class="dropdown dropdown-hover">
                <label tabindex="0" class="btn btn-xs m-1">...</label>
                  ${
                    (el.order.status === 1 &&
                      ` 
              <ul
                tabindex="0"
                class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52"
              >
            <li>
              <a
                class="text-primary"
                href="${url}/order_status?accept=${el.order.id}"
                ><i class="fa-regular fa-circle-check"></i>Accepet order</a
              >
            </li>
            <li>
              <a
                class="text-error"
                href="${url}/order_status?reject=${el.order.id}"
                ><i class="fa-regular fa-circle-xmark"></i> Reject order</a
              >
              </li>
            </ul>
            `) ||
                    ""
                  }
          </div>
        </div>
      </div>
      
          `;
          try {
            let span2 = document.createElement("span");
            span2.innerHTML = template;
            document.getElementById("recent").append(span2);
          } catch (error) {}
        });
      })
      .finally(() => {
        let edit_notif = document.querySelectorAll("[data-attr]");
        edit_notif.forEach((el) =>
          el.addEventListener("click", async (e) => {
            let notif_id = el.getAttribute("data-attr");
            await fetch(`${url}/notifications`, {
              mode: "cors",
              method: "POST",
              headers: {
                "content-type": "application/json",
              },
              body: JSON.stringify({ readed_notif_id: notif_id }),
            });

            console.log(notif_id);
          })
        );
      });
  }, 5000);
});

// <div class="avatar">
//   <div class="w-10 rounded-full">
//     <img src="https://placeimg.com/192/192/people" />
//   </div>
// </div>;
