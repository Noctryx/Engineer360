let chartInstance = null;

document.addEventListener("DOMContentLoaded", async () => {
  const userName = localStorage.getItem("userName");
  const role = localStorage.getItem("userRole");

  if (!userName || !role) {
    document.body.innerHTML =
      "<h2 style='text-align:center;margin-top:50px;'>Session expired. Please start again.</h2>";
    return;
  }

  document.getElementById("userInfo").innerText =
    `Hello ${userName} | Target Role: ${role.replaceAll("_", " ")}`;

  await fetchAnalysis();
});

async function fetchAnalysis() {
  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: localStorage.getItem("userName"),
        branch: localStorage.getItem("userBranch"),
        target_role: localStorage.getItem("userRole"),
        skills: JSON.parse(localStorage.getItem("selectedSkills") || "[]"),
        sleep_hours: parseFloat(localStorage.getItem("sleep")),
        stress_level: parseInt(localStorage.getItem("stress")),
        focus_score: parseInt(localStorage.getItem("focus")),
        study_hours: parseFloat(localStorage.getItem("study")),
      }),
    });

    if (!response.ok) {
      throw new Error("Backend error: " + response.status);
    }

    const data = await response.json();
    renderDashboard(data);
  } catch (error) {
    console.error("Error fetching analysis:", error);
    document.body.innerHTML =
      "<h2 style='text-align:center;margin-top:50px;'>Error loading report.</h2>";
  }
}

function renderDashboard(data) {
  const skillData = data.skill_analysis;
  const burnoutData = data.burnout_analysis;

  const matchPercent = skillData.match_percentage;

  document.getElementById("matchPercent").innerText = matchPercent + "% Match";

  const progressBar = document.getElementById("progressBar");
  progressBar.style.width = matchPercent + "%";

  progressBar.style.background =
    matchPercent >= 75 ? "#22c55e" : matchPercent >= 40 ? "#facc15" : "#ef4444";

  if (skillData.missing_skills && skillData.missing_skills.length > 0) {
    let html = "<strong>Missing Skills:</strong><ul>";

    const resources = data.learning_resources || {};

    skillData.missing_skills.slice(0, 4).forEach((item) => {
      const skillName = item.skill || item; // handle both formats
      const readable = skillName.replaceAll("_", " ");

      const link = resources[skillName] || "#";

      html += `
      <li>
        ${readable}
        <br>
        <a href="${link}"
           target="_blank"
           rel="noopener noreferrer"
           class="learn-link">
           ▶ Learn Now
        </a>
      </li>
    `;
    });

    html += "</ul>";

    document.getElementById("missingSkills").innerHTML = html;
  } else {
    document.getElementById("missingSkills").innerHTML =
      "<strong>Excellent! No missing skills 🎉</strong>";
  }

  const burnoutEl = document.getElementById("burnoutLevel");
  burnoutEl.innerText = `${burnoutData.burnout_risk} (${burnoutData.burnout_score}%)`;

  document.getElementById("burnoutAdvice").innerText =
    burnoutData.burnout_risk === "HIGH"
      ? "Immediate recovery recommended."
      : burnoutData.burnout_risk === "MODERATE"
        ? "Balance intensity and recovery."
        : "Healthy performance state.";

  document.getElementById("smartAdvice").innerText = data.final_recommendation;

  renderChart(matchPercent);
}

function renderChart(matchPercent) {
  const ctx = document.getElementById("skillChart").getContext("2d");

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Achieved", "Remaining"],
      datasets: [
        {
          data: [matchPercent, 100 - matchPercent],
          backgroundColor: ["#22c55e", "#ef4444"],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

document.getElementById("restartBtn").addEventListener("click", () => {
  localStorage.clear();
  window.location.href = "index.html";
});
