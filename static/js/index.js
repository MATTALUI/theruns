(async () => {
  const res = await fetch("/api/routes");
  const routes = await res.json();
  console.table(routes);
})();