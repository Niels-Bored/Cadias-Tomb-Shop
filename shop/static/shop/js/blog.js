function verDetallers(titulo, descripcion, urlImagen) {
    Swal.fire({
        title: titulo,
        html: `<b>${descripcion}`,
        imageUrl: urlImagen,
        imageWidth: 100,
        imageHeight: 100,
        icon: "info",
        confirmButtonText: "Aceptar"
    });

}

function actualizarContadorCarrito() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let totalCantidad = carrito.reduce((sum, producto) => sum + producto.cantidad, 0);

    let contador = document.getElementById("cart-count");
    contador.textContent = totalCantidad;

    // Mostrar/ocultar el círculo solo si hay productos
    contador.style.display = totalCantidad > 0 ? "block" : "none";
}

// Ejecutar la función al cargar la página
document.addEventListener("DOMContentLoaded", actualizarContadorCarrito);