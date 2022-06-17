function confirmarEliminacion(id,tipo) {
    Swal.fire({
        title: 'Estas seguro?',
        text: "no podras revertir esta accion!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: 'cancelar',
        confirmButtonText: 'confirmar!'
    }).then((result) => {
        if (result.value) {
            //redirigir al usuario a la ruta eliminar
            if (tipo === 'post'){
                window.location.href = "/eliminar_post/" + id ;
            }
            if (tipo === 'tiend'){
                window.location.href = "/eliminar_tienda/" + id ;
            }
            if (tipo === 'trab'){
                window.location.href = "/eliminar_trabajador/" + id ;
            }

        }
    })
}
// if (tipo === 'post'){
//     if (result.value) {
//         redirigir al usuario a la ruta eliminar
//         window.location.href = "/eliminar_post/" + id ;

//     }
// }
// if (tipo === 'tiend'){
//     if (result.value) {
//         redirigir al usuario a la ruta eliminar
//         window.location.href = "/eliminar_tienda/" + id ;
//     }
// }
// if (tipo === 'trab'){
//     if (result.value) {
//         redirigir al usuario a la ruta eliminar
//         window.location.href = "/eliminar_trabajador/" + id ;
//     }
// }