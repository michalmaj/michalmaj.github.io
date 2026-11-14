// Accessible section toggles in the navigation (Teaching Hub).
//
// The theme renders the control that expands or collapses a navigation section as
// <label class="md-nav__link" for="__nav_N" tabindex="0"> holding only an icon: it has no
// name, no role and no state, and Space does nothing (Enter works). The section's list is a
// <nav aria-labelledby> pointing at that label, so it has no name either. This script makes
// each toggle a named button whose aria-expanded follows the section, points it at the list
// it controls, and lets Space activate it like Enter.
//
// On narrow screens the navigation drawer and the search open from icons in the header, which
// are <label> elements without tabindex: keyboard users could not reach them. They become
// focusable buttons that open with Enter or Space; the drawer button reports aria-expanded.
//
// While the drawer is closed it is only moved off screen, so Tab still walked through its links.
// When the sidebar works as a drawer (narrow screens) and is closed, it is made inert: nothing in
// it can be focused or read until it opens. Escape closes an open drawer, and focus that was in
// the drawer returns to its button. On wide screens the sidebar is a column and stays as it is.
//
// The pipeline copies this file into every build and replaces the quoted placeholders with strings
// from data/i18n: nav_section_toggle ("Podsekcje: {name}"), and nav_drawer_button and
// search_button, used only when a header button has no text of its own (MkDocs Material).
(function () {
  "use strict";
  var NAME = "__TH_NAV_SECTION_TOGGLE__";
  var HEADER_NAMES = { __drawer: "__TH_NAV_DRAWER_BUTTON__", __search: "__TH_SEARCH_BUTTON__" };

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

  function headerButton(label) {
    var input = document.getElementById(label.htmlFor);
    if (!input) return;
    label.setAttribute("role", "button");
    if (!label.hasAttribute("tabindex")) label.setAttribute("tabindex", "0");
    if (!label.textContent.trim() && !label.hasAttribute("aria-label")) label.setAttribute("aria-label", HEADER_NAMES[label.htmlFor]);
    if (label.htmlFor === "__search") label.setAttribute("aria-haspopup", "dialog");
    if (label.htmlFor === "__drawer") {
      var sync = function () { label.setAttribute("aria-expanded", input.checked ? "true" : "false"); };
      sync();
      input.addEventListener("change", sync);
      label.addEventListener("click", function () { setTimeout(sync, 0); });
    }
    label.addEventListener("keydown", function (event) {
      if (event.key !== "Enter" && event.key !== " " && event.key !== "Spacebar") return;
      event.preventDefault(); // no page scroll on Space
      // The theme already handles Enter on focusable labels; click only if nothing happened.
      var before = input.checked;
      setTimeout(function () {
        if (input.checked === before) label.click();
      }, 0);
    });
  }

  function drawer() {
    var input = document.getElementById("__drawer");
    var sidebar = document.querySelector(".md-sidebar--primary");
    var button = document.querySelector('label.md-header__button[for="__drawer"]');
    if (!input || !sidebar) return;
    // The theme turns the sidebar into a fixed, off-screen drawer below its breakpoint.
    function isDrawer() {
      return getComputedStyle(sidebar).position === "fixed";
    }
    function update() {
      var closed = isDrawer() && !input.checked;
      if (closed && sidebar.contains(document.activeElement) && button) button.focus();
      if (closed) sidebar.setAttribute("inert", "");
      else sidebar.removeAttribute("inert");
    }
    function close() {
      input.checked = false;
      input.dispatchEvent(new Event("change", { bubbles: true }));
      if (button) button.focus();
    }
    update();
    input.addEventListener("change", update);
    // The theme may also change the drawer without a change event (e.g. on clicks); check after them.
    document.addEventListener("click", function () { setTimeout(update, 0); }, true);
    window.addEventListener("resize", update);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && input.checked && isDrawer()) close();
    });
  }

  document.querySelectorAll('label.md-nav__link[for^="__nav_"]').forEach(enhance);
  document.querySelectorAll('label.md-header__button[for="__drawer"], label.md-header__button[for="__search"]').forEach(headerButton);
  drawer();
})();
