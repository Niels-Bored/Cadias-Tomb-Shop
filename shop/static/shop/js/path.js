document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;
  
    const routes = {
      "/": "home-option",        // ← match exacto
      "/shop/": "shop-option",   // ← match parcial
      "/about/": "about-option",
      "/blog/": "blog-option",
      "/contact/": "contact-option"
    };
  
    let activeId = null;
  
    for (const route in routes) {
      const isRoot = route === "/";
  
      if ((isRoot && path === "/") ||                 // solo la home
          (!isRoot && path.includes(route))) {        // el resto
        activeId = routes[route];
        break;
      }
    }
  
    if (activeId) {
      const li = document.getElementById(activeId);
      li?.classList.add("active");
    }
  });
  