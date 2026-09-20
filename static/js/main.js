// main.js — students will add JavaScript here as features are built

document.addEventListener("DOMContentLoaded", function () {
    var FLASH_AUTO_DISMISS_MS = 10000;

    function dismissFlash(flash) {
        if (flash.dataset.dismissed === "true") return;
        flash.dataset.dismissed = "true";
        flash.classList.add("flash-message--hiding");
        flash.addEventListener("transitionend", function () {
            flash.remove();
        });
    }

    document.querySelectorAll(".flash-message").forEach(function (flash) {
        var timer = setTimeout(function () {
            dismissFlash(flash);
        }, FLASH_AUTO_DISMISS_MS);

        var closeBtn = flash.querySelector(".flash-close");
        if (closeBtn) {
            closeBtn.addEventListener("click", function () {
                clearTimeout(timer);
                dismissFlash(flash);
            });
        }
    });
});
