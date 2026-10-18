"use strict";
const stages = {
  collect: ["Start with evidence.", "Save the accessible source, its URL, capture time and processing status. A failed download remains a failed download, rather than silently becoming an empty document.", "Engineering pattern: provenance and explicit missing data"],
  question: ["Make the claim testable.", "Turn an observation into a hypothesis with a defined horizon, comparison and condition that would disprove it. Keep interpretation separate from the original source.", "Engineering pattern: falsifiers and pre-registered experiments"],
  test: ["Measure the whole experiment.", "Compare a paper account with a benchmark over the same window. Show the broader set of trials and negative outcomes so a selected winner cannot stand in for the entire experiment.", "Engineering pattern: benchmark alignment and selection context"],
  retain: ["Keep the useful lessons.", "Retain source-linked findings, failure records and reviewed operating instructions in Optimus. A future session can retrieve the relevant evidence; stored text does not automatically retrain a model.", "Engineering pattern: persistent retrieval and reviewed skills"]
};
for (const button of document.querySelectorAll("[data-stage]")) {
  button.addEventListener("click", () => {
    const item = stages[button.dataset.stage];
    for (const sibling of document.querySelectorAll("[data-stage]")) sibling.setAttribute("aria-pressed", String(sibling === button));
    const panel = document.getElementById("stage-content");
    panel.querySelector("h3").textContent = item[0];
    panel.querySelector("p").textContent = item[1];
    panel.querySelector(".stage-note").textContent = item[2];
  });
}
