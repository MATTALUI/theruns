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

  const parseTimeSeconds = (timeString) => {
    const regex = /^(\d{0,2}:)?(\d{0,2}:)?(\d{0,2}(\.\d*)?)?$/gi;
    if (!regex.test(timeString))
      throw new Error("inputted string does not match regex expectation: " + timeString);
    let seconds = 0;
    const sections = timeString.split(":").reverse();
    seconds += Math.round(parseFloat(sections[0] || 0));
    seconds += Math.round(parseFloat(sections[1] || 0)) * 60;
    seconds += Math.round(parseFloat(sections[2] || 0)) * 60 * 60;
    if (isNaN(seconds))
      throw new Error("inputted string produces NaN: " + timeString);
    return seconds
  }

  runForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const row = Array.from(contentContainer.querySelectorAll("input"))
      .reduce((r, input) => {
        r[input.name] = parseTimeSeconds(input.value);

        return r;
      }, {})
    const payload = {
      route_name: routeSelect.value,
      row,
    };
    loadingContainer.classList.remove("opacity");
    contentContainer.classList.add("opacity");
    const req = await fetch("/api/runs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    window.location.pathname ="/runs";
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
      input.name = split.col_name;
      input.required = "true";

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