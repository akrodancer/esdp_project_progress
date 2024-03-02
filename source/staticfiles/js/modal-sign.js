$(document).on('click', '#sign_in_submit', function(e) {
    var myData = {
        login: $("#login").val(),
        password: $("#password").val(),
    }
    e.preventDefault();
    $.ajax({
        headers: {"X-CSRFToken": '{{csrf_token}}'},
        type: 'POST',
        url: "{% url 'accounts:log_in' %}",
        contentType: 'application/json',
        data: JSON.stringify(myData),
        success: function(json) {
            
        }
    })
})