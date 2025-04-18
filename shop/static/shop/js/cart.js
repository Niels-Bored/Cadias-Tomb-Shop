function actualizarTotales() {
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    let subtotal = carrito.reduce((sum, prod) => sum + (prod.precio * prod.cantidad), 0);
    
    document.getElementById("subtotal").textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById("total").textContent = `$${subtotal.toFixed(2)}`; // Puedes agregar impuestos si es necesario
}

document.addEventListener("DOMContentLoaded", function () {
    actualizarTotales(); // Actualizar al cargar la página
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const tbody = document.getElementById("carrito-body");

    carrito.forEach((producto, index) => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td class="product-thumbnail">
          <img src="${producto.urlImagen}" alt="Image" class="img-fluid" style="width: 50px;">
        </td>
        <td class="product-name">
          <h2 class="h5 text-black">${producto.nombre}</h2>
        </td>
        <td>$${producto.precio}</td>
        <td>
          <div class="input-group mb-3 d-flex align-items-center quantity-container" style="max-width: 120px;">
            <div class="input-group-prepend">
              <button class="btn btn-outline-black decrease" type="button" data-index="${index}">&minus;</button>
            </div>
            <input type="text" class="form-control text-center quantity-amount" value="${producto.cantidad}" data-index="${index}">
            <div class="input-group-append">
              <button class="btn btn-outline-black increase" type="button" data-index="${index}">&plus;</button>
            </div>
          </div>
        </td>
        <td>$${(producto.precio * producto.cantidad)}</td>
        <td><button class="btn btn-black btn-sm delete" data-index="${index}">X</button></td>
      `;

      tbody.appendChild(fila);
    });

    // Agregar eventos a los botones de aumentar, disminuir y eliminar
    tbody.addEventListener("click", function (event) {
      const index = event.target.dataset.index;
      let recargar = false
      if (event.target.classList.contains("increase")) {
        if(carrito[index].cantidad < carrito[index].stock){
            carrito[index].cantidad++;
            recargar = true
        }else{
            Swal.fire({
                title: "Cantidad excedida",
                html: `Ha superado la cantidad máxima disponible de <b>${carrito[index].nombre}</b> <br>Cantidad: ${carrito[index].cantidad}`,
                imageUrl: carrito[index].urlImagen,
                imageWidth: 100,
                imageHeight: 100,
                icon: "error",
                confirmButtonText: "Aceptar",
                customClass: {
                  confirmButton: 'btn btn-warning'  // Fondo amarillo estilo Bootstrap
                },
                buttonsStyling: false  // ¡Esto es clave para que funcione tu clase Bootstrap!
              });
        }
      } else if (event.target.classList.contains("decrease") && carrito[index].cantidad > 1) {
        carrito[index].cantidad--;
        recargar = true
      } else if (event.target.classList.contains("delete")) {
        carrito.splice(index, 1);
        recargar = true
      }

      // Guardar cambios en localStorage y recargar la tabla
      if(recargar){
        localStorage.setItem("carrito", JSON.stringify(carrito));
        location.reload();
        actualizarTotales(); // Actualizar al cargar la página
      }
    });
  });