document.addEventListener("DOMContentLoaded", function () {
    const path = window.location.pathname;
    
    const routes = {
        "/": "home-option",
        "/shop/": "shop-option",
        "/about/": "about-option",
        "/blog/": "blog-option",
        "/contact/": "contact-option"
    };

    const activeId = routes[path];
    if (activeId) {
        const li = document.getElementById(activeId);
        if (li) {
            li.classList.add("active");
        }
    }
});
