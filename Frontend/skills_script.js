document.addEventListener("DOMContentLoaded", () => {
  loadSkills();

  const btn = document.getElementById("generateBtn");
  btn.addEventListener("click", generateReport);
});

async function loadSkills() {
  try {
    const role = localStorage.getItem("userRole");

    if (!role) {
      window.location.href = "index.html";
      return;
    }

    const response = await fetch("https://engineer360.onrender.com/roles");
    const data = await response.json();

    const skills = Object.keys(data[role] || {});
    const container = document.getElementById("skillsContainer");

    container.innerHTML = "";

    skills.forEach((skill) => {
      const label = document.createElement("label");

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.value = skill;

      label.appendChild(checkbox);
      label.append(" " + skill.replaceAll("_", " "));

      container.appendChild(label);
    });
  } catch (err) {
    console.error("Failed to load skills:", err);
  }
}

function generateReport() {
  const selectedSkills = [];

  document
    .querySelectorAll("#skillsContainer input:checked")
    .forEach((cb) => selectedSkills.push(cb.value));

  const sleep = document.getElementById("sleep").value;
  const stress = document.getElementById("stress").value;
  const focus = document.getElementById("focus").value;
  const study = document.getElementById("study").value;

  if (!sleep || !stress || !focus || !study) {
    alert("Please fill all metrics.");
    return;
  }

  localStorage.setItem("selectedSkills", JSON.stringify(selectedSkills));
  localStorage.setItem("sleep", sleep);
  localStorage.setItem("stress", stress);
  localStorage.setItem("focus", focus);
  localStorage.setItem("study", study);

  window.location.href = "dashboard.html";
}
