(async () => {
  const [
    _,
    routes,
  ] = await Promise.all([
    new Promise(res => setTimeout(res, 1000)),
    fetch("/api/routes").then(r => r.json()),
  ]);

  const runForm = document.querySelector("form");
  const routeSelect = document.querySelector("select#route");
  const splitTimes = document.querySelector("#split-times");
  const loadingContainer = document.querySelector("#loading-container");
  const contentContainer = document.querySelector("#content-container");
  routeSelect.innerHTML = "";
  routes.sort((a, b) => a.name.localeCompare(b.name)).forEach(route => {
    const option = document.createElement("option");
    option.innerHTML = route.name;
    option.value = route.name;
    routeSelect.appendChild(option)
  });

  runForm.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log("submitting form");
  });


  routeSelect.addEventListener("change", (e) => {
    const selectedRouteName = e.target.value;
    const route = routes.find(r => r.name === selectedRouteName);
    splitTimes.innerHTML = "";
    route.splits.sort((a, b) => a.number - b.number).forEach(split => {
      const container = document.createElement("div");
      const input = document.createElement("input");
      const label = document.createElement("label");

      container.classList.add("field");
      container.classList.add("label");
      container.classList.add("border");

      input.type = "text";
      input.name = route.col_name;

      label.innerHTML = split.name;

      container.appendChild(input);
      container.appendChild(label);
      splitTimes.appendChild(container);
    });
  });
  routeSelect.dispatchEvent(new Event("change"));

  loadingContainer.classList.add("opacity");
  contentContainer.classList.remove("opacity");
})();