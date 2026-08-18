// JOBOS sidebar popup (spec 28).
// Scans the active tab for form inputs, asks the backend how to fill each,
// and displays the autofill/block plan. Never submits without human review.

document.getElementById("detect").addEventListener("click", async () => {
  const status = document.getElementById("status");
  status.textContent = "Scanning...";
  const plan = document.getElementById("plan");
  plan.innerHTML = "";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const res = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const inputs = Array.from(document.querySelectorAll("input, select, textarea"));
      const seen = new Set();
      const labels = [];
      for (const el of inputs) {
        const label = (el.labels && el.labels[0] && el.labels[0].textContent)
          || el.placeholder || el.name || el.id || "";
        const key = label.toLowerCase().trim();
        if (key && !seen.has(key)) { seen.add(key); labels.push(label.trim()); }
      }
      return labels;
    },
  });
  const labels = res && res[0] && res[0].result ? res[0].result : [];
  if (!labels.length) { status.textContent = "No form fields detected."; return; }

  const msg = { type: "MAP_FIELDS", fields: labels };
  const resp = await chrome.runtime.sendMessage(msg);
  if (!resp || !resp.ok) { status.textContent = "Backend error: " + (resp && resp.error); return; }

  const actions = resp.data.actions;
  actions.forEach((a) => {
    const div = document.createElement("div");
    div.className = "action " + a.action;
    div.textContent = `${a.action}: ${a.field}` + (a.value ? ` -> ${a.value}` : "");
    plan.appendChild(div);
  });
  status.textContent = resp.data.review_required
    ? "Review required before submit (high-risk fields)."
    : "All fields mapped - review then submit manually.";
});
