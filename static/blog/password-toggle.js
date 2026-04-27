(function () {
  function bind(btn) {
    if (btn.dataset.passwordToggleBound) return;
    btn.dataset.passwordToggleBound = "1";
    btn.addEventListener("click", function () {
      var wrap = btn.closest(".password-wrap");
      if (!wrap) return;
      var inp = wrap.querySelector("input");
      if (!inp) return;
      var showPlain = inp.type === "password";
      inp.type = showPlain ? "text" : "password";
      wrap.classList.toggle("is-visible", showPlain);
      btn.setAttribute("aria-pressed", showPlain ? "true" : "false");
      var labelShow = btn.getAttribute("data-label-show") || "Parolni ko‘rsatish";
      var labelHide = btn.getAttribute("data-label-hide") || "Parolni yashirish";
      var nextLabel = showPlain ? labelHide : labelShow;
      btn.setAttribute("aria-label", nextLabel);
      btn.setAttribute("title", nextLabel);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".password-toggle").forEach(bind);
  });
})();
