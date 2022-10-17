document.addEventListener("DOMContentLoaded", () => {
  let breadcrumbs = document.getElementById("breadcrumbs");
  let { origin, pathname, search } = location;
  let svg = `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="w-4 h-4 mr-2 stroke-current"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>`;
  let li1 = document.createElement("li");
  let a1 = `<a href='${origin}'> ${svg}Home</a>`;
  li1.innerHTML = a1;
  let li2 = document.createElement("li");

  let a2 = `<a href='${origin}${pathname}'> ${svg}${pathname.replace(
    "/",
    ""
  )}</a>`;

  li2.innerHTML = a2;

  let li3 = document.createElement("li");
  let a3 = `<a href='${origin}/${pathname} ${svg}${search}'>${search.replace(
    "?",
    ""
  )}</a>`;

  li3.innerHTML = a3;
  breadcrumbs.append(li1);
  if (pathname === "/") return;

  breadcrumbs.append(li2);
  if (search === "") return;
  breadcrumbs.append(li3);
});
