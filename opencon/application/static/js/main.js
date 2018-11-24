$( document ).ready(function() {
    console.log( "ready!" );

    $("#check_mail").on('click', function(){
        var email = $('#id_email').val();
        $('#myModal').remove();
        $.ajax({
            type: 'GET',
            url: '/check_email/' + email,
            success: function(result){
                $('body').append(result);
                $('#myModal').modal();
            },
            error: function(xhr, ajaxOptions, thrownError){
                if(xhr.status == 404){
                    console.log('not a valid email');
                }
            }
        });
        console.log('ooooh');
    });

    $('#skip').on('click', function(){
        $('#myModal').modal('show');
    });

    if(window.location.href.indexOf('saved') != -1){
        $('#check_mail').remove();
        $('#id_email').prop('readonly', true);
    }

    if(window.location.href.indexOf('saved') == -1 && window.location.href.indexOf('rate') == -1 && $('#id_email').length &&  $('#id_email').val().length < 5){
        $('#overlapping_div').addClass('overlap');
    }

    $(".se-pre-con").fadeOut(1000);

    // https://web.archive.org/web/20170710193025/https://stackoverflow.com/questions/9712295/disable-scrolling-on-input-type-number
    // disable mousewheel on number input field when in focus (useful on rating form to prevent Chrome from changing the value when scrolling)
    $('form').on('focus', 'input[type=number]', function (e) {
        $(this).on('mousewheel.disableScroll', function (e) {
          e.preventDefault()
        })
    })
    $('form').on('blur', 'input[type=number]', function (e) {
        $(this).off('mousewheel.disableScroll')
    })

});

function remove_overlap(){
    $('.overlap').remove();
    var lowercase_email_string = $('#id_email').val().toLowerCase();
    $('#id_email').val(lowercase_email_string);
    // #todo -- more sophisticated lowercase logic may be implemented on the backend but it's probably not necessary at the moment
    $('#id_email').prop('readonly', true);
    $('#check_mail').remove();
}
