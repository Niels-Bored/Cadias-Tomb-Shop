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