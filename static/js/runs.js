(async () => {
  const loadSplitReport = async (runId) => {
    // await new Promise(res => setTimeout(res, 500));
    console.log("loadSplitReport", runId);
    const req = await fetch(`/api/reports/runs-pace?run_id=${runId}`);
    const report = await req.json();
    console.table(report);
    const detailsEle = document.querySelector(`details[data-id="${runId}"]`);
    const container = detailsEle.querySelector(".split-container");

    const img = document.createElement("img");
    img.src = report.src;

    container.innerHTML = "";
    container.appendChild(img);
  }

  const loadOverviewReport = async (runId) => {
    await new Promise(res => setTimeout(res, 500));
    console.log("loadOverviewReport", runId);
    const req = await fetch(`/api/reports/runs-overview?run_id=${runId}`);
    const report = await req.json();
    console.table(report);
    const detailsEle = document.querySelector(`details[data-id="${runId}"]`);
    const container = detailsEle.querySelector(".overview-container");

    const img = document.createElement("img");
    img.src = report.src;

    container.innerHTML = "";
    container.appendChild(img);
  }

  const loadReports = (event) => {
    const summaryEle = event.target;
    const detailsEle = summaryEle.closest("details");
    const splitContainer = detailsEle.querySelector(".split-container");
    const overviewContainer = detailsEle.querySelector(".overview-container");
    const runId = detailsEle.dataset.id;

    if (!splitContainer.querySelector('img')) loadSplitReport(runId);
    if (!overviewContainer.querySelector('img')) loadOverviewReport(runId);
  };

  document.querySelectorAll("summary").forEach((ele) => {
    ele.addEventListener("click", loadReports);
  });
})();