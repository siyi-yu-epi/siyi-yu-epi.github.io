/*
 * Progressive-enhancement tabs.
 *
 * Markup contract (see index.md):
 *   <div class="tabs" data-tabs>
 *     <div class="tab-panel" id="about" data-tab-title="About" markdown="1"> ... </div>
 *   </div>
 *
 * Without JavaScript every panel simply renders stacked, so the content is
 * never hidden from readers or crawlers.
 */
(function () {
  "use strict";

  function slugify(text) {
    return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  }

  function buildTabs(container) {
    var panels = Array.prototype.filter.call(
      container.children,
      function (child) {
        return child.hasAttribute("data-tab-title");
      }
    );
    if (panels.length < 2) {
      return;
    }

    var list = document.createElement("div");
    list.className = "tabs__list";
    list.setAttribute("role", "tablist");
    list.setAttribute("aria-label", container.getAttribute("data-tabs-label") || "Profile sections");

    var tabs = panels.map(function (panel, index) {
      var title = panel.getAttribute("data-tab-title");
      if (!panel.id) {
        panel.id = slugify(title);
      }

      var tab = document.createElement("button");
      tab.type = "button";
      tab.className = "tabs__tab";
      tab.id = panel.id + "-tab";
      tab.textContent = title;
      tab.setAttribute("role", "tab");
      tab.setAttribute("aria-controls", panel.id);

      panel.setAttribute("role", "tabpanel");
      panel.setAttribute("aria-labelledby", tab.id);
      panel.setAttribute("tabindex", "0");

      list.appendChild(tab);
      tab.addEventListener("click", function () {
        select(index, true);
      });
      return tab;
    });

    function select(index, updateHash) {
      tabs.forEach(function (tab, i) {
        var active = i === index;
        tab.setAttribute("aria-selected", active ? "true" : "false");
        tab.setAttribute("tabindex", active ? "0" : "-1");
        panels[i].hidden = !active;
      });
      if (updateHash && window.history && window.history.replaceState) {
        window.history.replaceState(null, "", "#" + panels[index].id);
      }
    }

    list.addEventListener("keydown", function (event) {
      var current = tabs.indexOf(document.activeElement);
      if (current === -1) {
        return;
      }
      var next = null;
      if (event.key === "ArrowRight") {
        next = (current + 1) % tabs.length;
      } else if (event.key === "ArrowLeft") {
        next = (current - 1 + tabs.length) % tabs.length;
      } else if (event.key === "Home") {
        next = 0;
      } else if (event.key === "End") {
        next = tabs.length - 1;
      }
      if (next !== null) {
        event.preventDefault();
        tabs[next].focus();
        select(next, true);
      }
    });

    container.insertBefore(list, container.firstChild);
    container.classList.add("tabs--enhanced");

    var requested = panels.findIndex(function (panel) {
      return "#" + panel.id === window.location.hash;
    });
    select(requested === -1 ? 0 : requested, false);
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-tabs]"), buildTabs);
  }

  // This file is loaded with `defer`, so parsing is normally already finished by
  // the time it runs. Enhancing right away avoids a flash of all four panels.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
