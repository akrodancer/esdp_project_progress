 //-------------------ЗАКРЫТИЕ МОДАЛЬНЫХ ОКОН----------------------//
 $("#back").on('click', function(e) {
     $('body').css('overflow', 'scroll');
     e.preventDefault();
     $(".turn-on").prop('hidden', 'true')
     $(".sign-up").prop('hidden', 'true')
 });
 $("#close").on('click', function(e) {
    $(".confirm").prop('hidden', 'true')
    $(".form-cover").prop('hidden', 'true')
});

 //-------------------МОДАЛЬНОЕ ОКНО ЛОГИНА----------------------//
 $("#sign_in_button").on('click', function(e) {
     $('body').css('overflow', 'hidden')
     e.preventDefault();
     $(".turn-on").removeAttr('hidden')
 });

  //-------------------МОДАЛЬНОЕ ОКНО ЗАЯВКИ----------------------//
 $("#sign_up_button").on('click', function(e) {
    $('body').css('overflow', 'hidden')
    e.preventDefault();
    $(".sign-up").removeAttr('hidden')
});

 //-------------------МЕТОД ОТПРАВКИ ЗАПРОСА----------------------//
$('#course_sign').on('click', function(e) {
    let rawData = {
        first_name: $('#first_name').val(),
        last_name: $('#last_name').val(),
        phone: $('#phone').val(),
        email: $('#email').val(),
        course: $('#course').val(),
    };
    $.ajax({
        headers: {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value},
        type: 'POST',
        url: 'accounts/sign_up/',
        contentType: 'application/json',
        data: JSON.stringify(rawData),
        success: function(json) {
            $(".form-cover").removeAttr('hidden')
            $(".confirm").removeAttr('hidden')
        }
    });
    e.preventDefault();
})

