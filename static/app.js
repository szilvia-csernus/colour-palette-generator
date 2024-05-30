const form = document.getElementById("form");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  getColors();
});

function getColors() {
  const formData = new FormData(form);

  fetch("/palette", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("extracted data", data);
      const colors = data.colors;
      const container = document.querySelector(".container");
      createColorBoxes(colors, container);
    });
}

function createColorBoxes(colors, container) {
  container.innerHTML = "";
      for (const color of colors) {
        const div = document.createElement("div");
        div.classList.add("color");
        div.style.width = `calc(100% / ${colors.length})`;
        div.style.backgroundColor = color;

        div.addEventListener("click", () => {
          navigator.clipboard.writeText(color);
          alert(`Copied ${color} to clipboard`);
        });

        const span = document.createElement("span");
        span.textContent = color;
        div.appendChild(span);
        container.appendChild(div);
      }
}
