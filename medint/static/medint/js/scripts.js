// JavaScript Document
var _height;
var _width;
var docHeight;
var i=1;
var angle=0;
var delay;
var IE = $.browser.msie;
var background;
var position 	= {"":0, "main":0, "login":0.8,"register":0.8};
var target="";
var hash="";
var oldtarget="";
var logoPW;
var phone = false;
var btnRegL;



var getHash= function() {
    return location.hash.replace('#!/', '');
}
	
	
	
$(document).ready(function(e) {
    if(IE){
        window.location = "install_chrome.html";
    }

	$('.bkg').hide();
	$('#logo,#loginb,#who,footer,#login,#register,#invite_code_doctor,#invite_code_patient,#not_invite_code_doctor,#not_invite_code_patient,#doctor_register,#patient_register,#forget').hide();
	$('.alert').hide();
	$('body').removeClass('hidden');
	background 	= $('#background img');
	_width = document.body.clientWidth;
	_height = $(window).height();
	docHeight = $(document).height();
	background.css('top',0);
	logoPW = $('#logoP').width();
	
	if( navigator.userAgent.match(/(iPhone)|(iPod)|(blackberry)|(smartphone)|(nexus one)|(htc)|(mobile_safari)|(phone)/i)){
		$('#logo,#loginb,#who').fadeIn();
		phone = true;
	}
	
	if(_width<768){
        var hLog = $('#ctLogin').height();
        $('#box').css('height',hLog);
    }

    changeSection();
    positions();

	function changeSection(){
        hash = window.location.hash;
        target = getHash();

        if (!$('#logo').is(':visible')){
            $('#logo').delay(1000).fadeIn(600);
        }

		if(target=="main" || target==""){
			$('footer').hide();
			$('.bkg').delay(1500).fadeIn('slow');
			$('#loginb').delay(2000).fadeIn(600);
			$('#who').delay(2300).fadeIn('slow');
			$('footer').delay(2500).fadeIn('slow');
			if(oldtarget !="" && oldtarget!="main"){
				$('#'+oldtarget).fadeOut('slow');
			}
		}
		

		if(target=="register" || target=="login"){
			if(oldtarget !="" && oldtarget!="main"){
				$('#'+oldtarget).delay(200).fadeOut('slow');
				$('footer').hide();
			}
			$('#who').fadeOut('fast');
			$('.bkg').fadeOut('fast');
			$('#loginb').fadeOut("fast");
			
			$('#'+target).delay(1200).fadeIn('slow');
			$('footer').delay(2000).fadeIn('slow');
			
		}
		if(target=="invite_code_doctor" || target=="invite_code_patient" ||
            target=="not_invite_code_doctor" || target=="not_invite_code_patient" ||
            target=="doctor_register" || target=="patient_register" || target=="forget") {
			
			if(oldtarget !="" && oldtarget!="main"){
				$('#'+oldtarget).delay(200).fadeOut('slow');
				$('footer').hide();
			}

            $('#who').fadeOut('fast');
			//$('footer').fadeOut('fast');
			$('.bkg').fadeOut('fast');
			$('#loginb').fadeOut("fast");
			
			$('#'+target).delay(1200).fadeIn('slow', function(){
                $('input[type="text"], input[type="password"]', '#' + target).first().focus();
            });
			$('footer').delay(2000).fadeIn('slow');
			
			
		}
		$('#'+target).addClass('activate');
		$('#'+oldtarget).addClass('activate');
		oldtarget = target;
	}

    function positions(){
        docHeight = $(document).height();
        var alertW = Math.round(0.955*_width);

        if(_width<768){
            var hLog = $('#ctLogin').height();
            $('#box').css('height',hLog);

        }

        if(_height>300 && _height<650){
            $('#login').css('top',130);
        }

        if(_height>=650 && _height<800){
            if(phone!=true){
                $('#logo').css('margin-top',60);
            }
            $('.sections').css('top',170);
            $('#login').css('top',150);
            $('#register').css('top',170);
        }
    }
	
	$(window).resize(function(){
		_width = document.body.clientWidth;
		_height = $(document).height();
		
		positions();
		
		if(phone!=true){
		    bottomBkg = Math.round((($(window).height()+50)-background.height())*position[target]);
		
            if( $(window).width() < 1200 && $(window).width() > 768){
                background.attr('width',1200);background.css({left:((_width)-background.width())*0.5});
            }else{
                background.attr('width','100%');background.css({left:0});
            }
            background.css('bottom',bottomBkg);
		}
	});

    $(window).on('hashchange', changeSection);

    $('#lost-password-form').submit(function(){
        $.ajax({
            data : $(this).serializeObject(),
            url : '/api/medint/lostPassword',
            dataType : 'json',
            type : 'POST',
            success : function(json){
                if('ok' == json.result){
                    success('Recovery mail sent');
                } else {
                    error(json.description);
                }
            }
        });
        return false;
    });

    $('#medicalSignup').submit(function(){
        var f = this;
        if ($(this).validate()) {
            var data = $(this).serializeObject();
            $.ajax({
                url: '/api/medint/saveAddress',
                type: 'POST',
                dataType: 'json',
                data: data,
                success: function (json) {
                    if ('ok' == json.result) {
                        f.reset();
                        //success('Your email has been added to our list. You will be notified soon !');
                        window.location = '/saved_email';
                        //$('#saved_email').show(50);
                    } else {
                        $.error(json.description);
                    }
                }
            });
        }
        return false;
    });

    $('#login-form').submit(function(){
        try{
            var $form = $(this);
            $form.disableForm();

            var data = $form.serializeObject();

            var res = $.rest.create('/api/login', data);
            $form.enableForm();
            if(res.isOk){
                window.location='/';
            } else {
                if (null == res.validationErrors){
                    error(res.error);
                } else{
                    $(this).showValidationErrors(res.validationErrors);
                }
            }
        } catch (e){
            console.log(e);
        }
        return false;
    });
	
	$('#patientRegisterForm').submit(function(){
        var $form = $(this);
        if ($form.validate()) {
            $form.disableForm();
            var data = $form.serializeObject();
            try{
                var res = $.rest.create('/api/medint/register', data);
                $form.enableForm();
                if(res.isOk){
                    window.location = '/register';
//                    success('Your account has been registered');
                } else {
                    if (null == res.validationErrors){
                        error(res.error);
                    } else{
                        $(this).showValidationErrors(res.validationErrors);
                    }
                }
            } catch(e){
                console.log(e);
            }
        }
        return false;
    });

    $('#doctorRegisterForm').submit(function(){
        var $form = $(this);
        if ($form.validate()) {
            $form.disableForm();
            var data = $form.serializeObject();
            try{
                var res = $.rest.create('/api/medint/register', data);
                $form.enableForm();
                if(res.isOk){
                    window.location = '/register';

                } else {
                    if (null == res.validationErrors){
                        error(res.error);
                    } else{
                        $(this).showValidationErrors(res.validationErrors);
                    }
                }
            } catch(e){
                console.log(e);
            }
        }
        return false;
    });

    $('.otp-form').submit(function(){
        $(this).disableForm();
        try{
            var data = $(this).serializeObject();
            var res = $.rest.get('/api/checkotp', data);

            if(res.isOk){
                if(3 == data.role){
                    $('#doctorRegisterForm').resetForm();
                    $('input[name="yubiid"]', '#doctorRegisterForm').val(data.otp.substring(0, 12));
                    window.location = '#!/doctor_register';
                }
                if(4 == data.role){
                    $('#patientRegisterForm').resetForm();
                    $('input[name="yubiid"]', '#patientRegisterForm').val(data.otp.substring(0, 12));
                    window.location = '#!/patient_register';
                }
            } else {
                if (null == res.validationErrors){
                    console.log('ERR:'  + res.error);
                    error(res.error);
                } else{
                    $(this).showValidationErrors(res.validationErrors);
                }
            }
            $(this).enableForm();
        } catch (e){
            console.log(e);
        }

        return false;
    })

});