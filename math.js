const display = document.getElementById("display");
let memory = 0;

function appendValue(value) {
  display.value += value;
}

function clearDisplay() {
  display.value = "";
}

function calculate() {
  try {
    let expression = display.value;

    expression = expression.replace(/sin\(/g, "Math.sin(");
    expression = expression.replace(/cos\(/g, "Math.cos(");
    expression = expression.replace(/log\(/g, "Math.log10(");

    display.value = eval(expression);
  } catch {
    display.value = "Error";
  }
}

function memoryAdd() {
  const currentValue = Number(display.value);

  if (!isNaN(currentValue)) {
    memory += currentValue;
  }
}

function memorySubtract() {
  const currentValue = Number(display.value);

  if (!isNaN(currentValue)) {
    memory -= currentValue;
  }
}

function toggleTheme() {
  document.body.classList.toggle("dark");
}

document.addEventListener("keydown", function(event) {
  const key = event.key;

  if (!isNaN(key) || ["+", "-", "*", "/", ".", "(", ")"].includes(key)) {
    appendValue(key);
  } else if (key === "Enter") {
    calculate();
  } else if (key === "Backspace") {
    display.value = display.value.slice(0, -1);
  } else if (key === "Escape") {
    clearDisplay();
  }
});
