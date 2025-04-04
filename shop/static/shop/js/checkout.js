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

function cargarProductosOrden() {
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const orderBody = document.getElementById("order-body");
    orderBody.innerHTML = ""; // Limpiar tabla antes de actualizar

    let subtotal = 0;

    carrito.forEach(producto => {
      const fila = document.createElement("tr");
      const totalProducto = producto.precio * producto.cantidad;
      subtotal += totalProducto;

      fila.innerHTML = `
        <td>${producto.nombre} <strong class="mx-2">x</strong> ${producto.cantidad}</td>
        <td>$${totalProducto}</td>
      `;
      orderBody.appendChild(fila);
    });

    // Agregar fila de subtotal
    const filaSubtotal = document.createElement("tr");
    filaSubtotal.innerHTML = `
      <td class="text-black font-weight-bold"><strong>Subtotal</strong></td>
      <td class="text-black">$${subtotal}</td>
    `;
    orderBody.appendChild(filaSubtotal);

    // Agregar fila de total
    const filaTotal = document.createElement("tr");
    filaTotal.innerHTML = `
      <td class="text-black font-weight-bold"><strong>Total</strong></td>
      <td class="text-black font-weight-bold"><strong>$${subtotal}</strong></td>
    `;
    orderBody.appendChild(filaTotal);
  }

  document.addEventListener("DOMContentLoaded", cargarProductosOrden);

  