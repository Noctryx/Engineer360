document.addEventListener("DOMContentLoaded", () => {
  const branchSelect = document.getElementById("branch");
  const roleSelect = document.getElementById("role");
  const form = document.getElementById("onboardingForm");

  async function loadBranches() {
    try {
      const response = await fetch("https://engineer360.onrender.com/branches");
      const data = await response.json();

      Object.keys(data).forEach((branch) => {
        const option = document.createElement("option");
        option.value = branch;
        option.textContent = branch;
        branchSelect.appendChild(option);
      });
    } catch (err) {
      console.error("Failed to load branches:", err);
    }
  }

  branchSelect.addEventListener("change", async () => {
    const branch = branchSelect.value;
    roleSelect.innerHTML = '<option value="">-- Choose Role --</option>';

    if (!branch) return;

    try {
      const response = await fetch("https://engineer360.onrender.com/roles");
      const data = await response.json();

      let roles = data[branch] || [];
      roles = [...roles, "DATA_ANALYST"];

      roles.forEach((role) => {
        const option = document.createElement("option");
        option.value = role;
        option.textContent = role.replaceAll("_", " ");
        roleSelect.appendChild(option);
      });
    } catch (err) {
      console.error("Failed to load roles:", err);
    }
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const branch = branchSelect.value;
    const role = roleSelect.value;

    if (!name || !branch || !role) {
      alert("Please fill all fields.");
      return;
    }

    localStorage.setItem("userName", name);
    localStorage.setItem("userBranch", branch);
    localStorage.setItem("userRole", role);

    window.location.href = "skills.html";
  });

  loadBranches();
});
