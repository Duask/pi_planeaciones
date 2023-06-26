$(document).ready(function() {
  $('#tuFormulario').submit(function(event) {
    event.preventDefault();
    var formData = $(this).serialize();

    $.ajax({
      type: 'POST',
      url: '/area',
      data: formData,
      success: function(response) {
        if (response.status === 'success') {
          Swal.fire("Error", "El usuario ya existe", "error");
        } else {
            var responseData = $(response).find('#areas-container').html();
          // Eliminar solo los datos antiguos del contenedor
          $('#areas-container').empty().html(responseData);

          Swal.fire({
            title: "El maestro fue agregado correctamente",
            icon: "success",
            showConfirmButton: false,
            timer: 3000,
          });
        }
      },
      error: function(xhr, status, error) {
        console.error(error);
      }
    });
  });
});

  

  
//request para eliminar un area

  $(document).ready(function() {
    $('.delete-area-btns').click(function() {
      var areaId = $(this).data('area-id');
      
      var $button = $(this); // Almacenar una referencia al botón para su uso dentro de la función success
      const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
      })
      swalWithBootstrapButtons.fire({
        title: '¿Estás seguro?',
        text: '¡No podrás revertir esto!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, borrarlo',
        cancelButtonText: 'No, cancelar',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          console.log(areaId)
          $.ajax({
            type: 'GET',
            url: '/area/' + areaId,
              success: function (response) {
                var responseData = $(response).find('#areas-container').html();
                $('#areas-container').empty().html(responseData);

              $button.closest('.areas-container').remove();
              swalWithBootstrapButtons.fire(
                '¡Eliminado!',
                'Tu archivo ha sido eliminado.',
                'success'
                );
                
            },
            error: function() {
              swalWithBootstrapButtons.fire(
                'Error',
                'Ocurrió un error al eliminar el área.',
                'error'
              );
            }
          });
        } else if (result.dismiss === Swal.DismissReason.cancel) {
          swalWithBootstrapButtons.fire(
            'Cancelado',
            'Tu archivo imaginario está a salvo :)',
            'error'
          );
        }
      });
    });
  });