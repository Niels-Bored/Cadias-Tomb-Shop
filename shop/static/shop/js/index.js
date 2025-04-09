function agregarAlCarrito(id, nombre, urlImagen, precio, marca, stock) {
    // Obtener el carrito actual desde localStorage (o crear uno vacío)
    let agregado = false

    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    // Buscar si el producto ya está en el carrito
    let productoExistente = carrito.find(p => p.id === id);

    if (productoExistente) {
        // Si ya está en el carrito, aumentar la cantidad, a menos que se supere el stock
        if(productoExistente.cantidad<stock){
            productoExistente.cantidad += 1;
            agregado = true
        }
        
    } else {
        // Si es un producto nuevo, agregarlo con cantidad 1
        carrito.push({
            id: id,
            nombre: nombre,
            urlImagen: urlImagen,
            precio: precio,
            marca: marca,
            cantidad: 1,
            stock: stock
        });
        agregado = true
    }

    // Guardar el carrito actualizado en localStorage
    localStorage.setItem('carrito', JSON.stringify(carrito));
    
    actualizarContadorCarrito()

    // Mostrar SweetAlert con información del producto
    if(agregado){
        Swal.fire({
            title: "Producto añadido 🛒",
            html: `<b>${nombre}</b> ha sido añadido al carrito.<br>Cantidad: ${productoExistente ? productoExistente.cantidad : 1}`,
            imageUrl: urlImagen,
            imageWidth: 100,
            imageHeight: 100,
            icon: "success",
            confirmButtonText: "Aceptar"
        });
    }else{
        Swal.fire({
            title: "Cantidad excedida",
            html: `Ha superado la cantidad máxima disponible de <b>${nombre}</b> <br>Cantidad: ${productoExistente.cantidad}`,
            imageUrl: urlImagen,
            imageWidth: 100,
            imageHeight: 100,
            icon: "error",
            confirmButtonText: "Aceptar"
        });
    }
}

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
