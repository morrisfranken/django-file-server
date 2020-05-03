function failLogin(message) {
	$("#message").html(message);
	$('.wrapper').removeClass('form-success');
	$('form').fadeIn(200);
}

$("#login-button").click(function(event){
	event.preventDefault();

	var email = $("#txt_uname").val().trim();
	var password = $("#txt_pwd").val().trim();

	if( email != "" && password != "" ){
        $('form').fadeOut(300);
        $('.wrapper').addClass('form-success');

		$.ajax({
			url:'/users/login',
			type:'post',
			data:{email:email,password:password, csrfmiddlewaretoken:csrfmiddlewaretoken},
			success:function(response){
				var url = new URL(window.location.href);
				var next = url.searchParams.get("next");
				window.location = next || "/";
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				failLogin(XMLHttpRequest["responseJSON"]["message"]);
			}
		});
	}
});
