const generateBtn = document.getElementById("generateBtn");
const tripInput = document.getElementById("tripInput");
const resultSection = document.getElementById("result");
const planBox = document.getElementById("planBox");
const errorBox = document.getElementById("errorBox");

generateBtn.addEventListener("click", async () => {
  const input = tripInput.value.trim();
  if (!input) {
    showError("⚠️ Please enter your trip details!");
    return;
  }

  clearError();
  generateBtn.disabled = true;
  generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin spinner"></i> Generating...';

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ trip_details: input })
    });

    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

    const data = await res.json();

    if (data.error) {
      showError("❌ " + data.error);
    } else {
      resultSection.style.display = "block";
      planBox.innerHTML = data.plan.replace(/\n/g, "<br/>");
      resultSection.classList.add("fade-in");
      resultSection.scrollIntoView({ behavior: 'smooth' });
    }
  } catch (err) {
    showError("⚠️ Something went wrong: " + err.message);
    console.error(err);
  } finally {
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<span>✨ Generate Plan</span>';
  }
});

function showError(msg) {
  errorBox.style.display = "block";
  errorBox.innerText = msg;
}

function clearError() {
  errorBox.style.display = "none";
  errorBox.innerText = "";
}
