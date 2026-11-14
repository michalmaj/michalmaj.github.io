// Accessible section toggles in the navigation (Teaching Hub).
//
// The theme renders the control that expands or collapses a navigation section as
// <label class="md-nav__link" for="__nav_N" tabindex="0"> holding only an icon: it has no
// name, no role and no state, and Space does nothing (Enter works). The section's list is a
// <nav aria-labelledby> pointing at that label, so it has no name either. This script makes
// each toggle a named button whose aria-expanded follows the section, points it at the list
// it controls, and lets Space activate it like Enter.
//
// The pipeline copies this file into every build and replaces the quoted placeholder with the
// toggle name from data/i18n (nav_section_toggle, e.g. "Podsekcje: {name}").
(function () {
  "use strict";
  var NAME = "__TH_NAV_SECTION_TOGGLE__";

  function sectionName(label) {
    var container = label.closest(".md-nav__container") || label.parentElement;
    var link = container && container.querySelector("a.md-nav__link");
    return link ? link.textContent.trim() : "";
  }

  function enhance(label) {
    var input = document.getElementById(label.htmlFor);
    if (!input || input.type !== "checkbox") return;
    var item = input.closest(".md-nav__item");
    var list = item && item.querySelector(":scope > nav.md-nav");
    var name = label.textContent.trim() || sectionName(label);

    label.setAttribute("role", "button");
    if (name) label.setAttribute("aria-label", NAME.replace("{name}", name));
    if (list) {
      if (!list.id) list.id = label.htmlFor + "_list";
      label.setAttribute("aria-controls", list.id);
    }
    function sync() {
      label.setAttribute("aria-expanded", input.checked ? "true" : "false");
    }
    sync();
    input.addEventListener("change", sync);
    if (list) new MutationObserver(sync).observe(list, { attributes: true, attributeFilter: ["aria-expanded"] });
    label.addEventListener("keydown", function (event) {
      if ((event.key === " " || event.key === "Spacebar") && !event.defaultPrevented) {
        event.preventDefault(); // no page scroll
        label.click();
        sync();
      }
    });
  }

  document.querySelectorAll('label.md-nav__link[for^="__nav_"]').forEach(enhance);
})();
