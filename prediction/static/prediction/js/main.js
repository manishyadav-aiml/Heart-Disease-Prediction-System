document.addEventListener("DOMContentLoaded", function () {
  // Fade out status messages after a few seconds
  document.querySelectorAll(".messages .message").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity .6s";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 700);
    }, 6000);
  });

  // Animate the marker on the result gauge
  var marker = document.querySelector(".gauge-marker");
  if (marker) {
    var value = parseFloat(marker.dataset.left);
    if (!isNaN(value)) {
      value = Math.max(0, Math.min(100, value));
      setTimeout(function () { marker.style.left = "calc(" + value + "% - 2px)"; }, 100);
    }
  }

  // Prevent double submission of the prediction form
  var form = document.getElementById("predict-form");
  var button = document.getElementById("predict-btn");
  if (form && button) {
    form.addEventListener("submit", function () {
      button.disabled = true;
      button.textContent = "Predicting...";
    });
  }
});
