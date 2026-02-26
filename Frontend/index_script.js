document.addEventListener("DOMContentLoaded", () => {
  const branchSelect = document.getElementById("branch");
  const roleSelect = document.getElementById("role");
  const form = document.getElementById("onboardingForm");

  const BASE_URL = "https://engineer360.onrender.com";

  // ===============================
  // LOAD ALL BRANCHES
  // ===============================
  async function loadBranches() {
    try {
      const response = await fetch(`${BASE_URL}/branches`);
      const data = await response.json();

      branchSelect.innerHTML = '<option value="">-- Choose Branch --</option>';

      data.branches.forEach((branch) => {
        const option = document.createElement("option");
        option.value = branch;
        option.textContent = branch.replaceAll("_", " ");
        branchSelect.appendChild(option);
      });
    } catch (error) {
      console.error("Error loading branches:", error);
      alert("Unable to load branches. Please try again later.");
    }
  }

  // ===============================
  // LOAD ROLES BASED ON BRANCH
  // ===============================
  async function loadRoles(branch) {
    try {
      const response = await fetch(`${BASE_URL}/roles/${branch}`);
      const data = await response.json();

      roleSelect.innerHTML = '<option value="">-- Choose Role --</option>';

      data.roles.forEach((role) => {
        const option = document.createElement("option");
        option.value = role;
        option.textContent = role.replaceAll("_", " ");
        roleSelect.appendChild(option);
      });
    } catch (error) {
      console.error("Error loading roles:", error);
      alert("Unable to load roles. Please try again.");
    }
  }

  // ===============================
  // EVENT: BRANCH CHANGE
  // ===============================
  branchSelect.addEventListener("change", () => {
    const selectedBranch = branchSelect.value;

    roleSelect.innerHTML = '<option value="">-- Choose Role --</option>';

    if (!selectedBranch) return;

    loadRoles(selectedBranch);
  });

  // ===============================
  // FORM SUBMISSION
  // ===============================
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

  // ===============================
  // INITIAL LOAD
  // ===============================
  loadBranches();
});
