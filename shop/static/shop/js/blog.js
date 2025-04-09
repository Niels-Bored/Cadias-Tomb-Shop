function verDetallers(titulo, descripcion, urlImagen) {
    Swal.fire({
        title: titulo,
        html: `<b>${descripcion}`,
        imageUrl: urlImagen,
        imageWidth: 100,
        imageHeight: 100,
        icon: "info",
        confirmButtonText: "Aceptar",
            customClass: {
              confirmButton: 'btn btn-warning'  // Fondo amarillo estilo Bootstrap
            },
            buttonsStyling: false  // ¡Esto es clave para que funcione tu clase Bootstrap!
    });

}