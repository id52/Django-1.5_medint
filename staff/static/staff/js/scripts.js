// JavaScript Document
var _height;
var _width;
var docHeight;
var footerL;
var i=1;
var angle=0;
var delay;
var ray;
var cnv;
var cnv2;
//var oldIE = $.browser.msie && $.browser.version <= 8;

var IE = navigator.userAgent.toLowerCase().indexOf('msie')!=-1;

var target="";
var hash="";
var $topLoader;
var oldtarget="";
var logoPW;
var topRegister;
var topLogin;
var phone = false;
var btnSignL;
var btnRegL;



var getHash= function() {
		return location.hash.replace('#!/', '');
	}
	
	
	
$(document).ready(function(e) {
	$('.bkg').hide();
	$('#logo,#loginb,footer,#login,#register,#staff_register,#not_invite_code').hide();
	$('body').removeClass('hidden');
	_width = document.body.clientWidth;
	_height = $(window).height();
	docHeight = $(document).height();
	footerL = Math.round((_width-500)/2);
    $('footer').css('left',footerL);
	
	
    $(window).bind('hashchange', function(e) {
        hash = window.location.hash;
        target = getHash();
	   changeSection();

    });
	
	if( navigator.userAgent.match(/(iPhone)|(iPod)|(blackberry)|(smartphone)|(nexus one)|(htc)|(mobile_safari)|(phone)/i)){
		$('#logo,#loginb,#who').fadeIn();
		phone = true;
	}
	
	if(IE){
		window.location = "install_chrome.html";
	}

    if(_width<768){
        var hLog = $('#ctLogin').height();
        $('#box').css('height',hLog);

    }


    changeSection();

	positions();

    function callLoginForm(){
        $("#ctPanel").empty();
        $.ajax({
            /*url:"/static/include/login.html",*/
            url:"static/include/login.html",
            success:function(data){
                $('#ctPanel').html(data);
            }
        });
        return false;
    }

    function changeSection(){
        if(target=="" || target=="main"){
            $('#main').delay(1200).fadeIn('slow');
            $('footer').hide();
            $('#logo').delay(1000).fadeIn(600);
            $('.bkg').delay(1500).fadeIn('slow');
            $('#loginb').delay(2000).fadeIn(600);
            $('footer').delay(2500).fadeIn('slow');
            if(oldtarget !="" && oldtarget!="main"){
                $('#'+oldtarget).fadeOut('slow');
            }
            target="main";
        }

        else{
            console.log('oldtarget :'+oldtarget);
            console.log('target :'+target);

            $('#'+oldtarget).delay(200).fadeOut('slow');

            $('#'+target).delay(1200).fadeIn('slow');
        }

        oldtarget = target;
    }

    function positions(){
        docHeight = $(document).height();
        var alertW = Math.round(0.955*_width);
        $('footer').css('position','absolute');
        $('footer').css('bottom',20);
        $('footer').css('left',footerL);
        $('footer').css('top','auto');


        if(_width<768){
            var hLog = $('#ctLogin').height();
            $('#box').css('height',hLog);

        }

        if(_height>300 && _height<650){
            if(target =="main" || target ==""){
                var topF = 477;
            }
            if(target=="register"){
                var topF = 600;
            }
            $('#login').css('top',130);
            $('footer').css('position','relative');
            $('footer').css('left',0);
            $('footer').css('bottom','auto');

        }

        if(_height>800){
            if(target=="main" ||target!=""){
                $('footer').css('position','absolute');
                $('footer').css('bottom',20);
                $('footer').css('left',footerL);
                $('footer').css('top','auto');
                //$('#main').css('top',80);
            }
        }

        if(_height>=650 && _height<800){
            if(phone!=true){
                $('#logo').css('margin-top',60);
            }
            $('.sections').css('top',170);
            $('#login').css('top',150);
            $('#register').css('top',170);
            //$('#logoP').css('top',20);

        }



        if(phone == true){
            //var btnSignL = Math.round(($('#ctLogin').width()-140)*0.5);
            btnSignL = Math.round(((_width*0.80)-113)*0.5);
            btnRegL = Math.round(((_width*0.95)-113)*0.5);
            $('footer').css('position','relative');
            $('footer').css('bottom','auto');
            $('footer').css('left','auto');
            $('footer').css('top','auto');
            //$('#logoP').css('left',0);
            //$('#btn-sign').css('margin-left',btnSignL);
            $('#ctRPanel #btn-register').css('margin-left',btnRegL);
        }


    }
	


	$(window).resize(function(){
		_width = document.body.clientWidth;
		_height = $(document).height();
		
		footerL = Math.round((_width-500)/2);
		$('#loader').css('left',((_width/2)-80));
		positions();
		
		if(phone!=true){
		
		}
		
		if(phone == true){
			//var btnSignL = Math.round(($('#ctLogin').width()-140)*0.5);
			var btnSignL = Math.round(((_width*0.80)-113)*0.5);
			btnRegL = Math.round(((_width*0.95)-113)*0.5);
			//$('#btn-sign').css('margin-left',btnSignL);
			$('#ctRPanel #btn-register').css('margin-left',btnRegL);
		}
		
	});

    $('#logoF').live('click',function(e){
        window.location='#!/login';
    });

    $('#staffRegisterForm').submit(function(){
        var $form = $(this);
        if ($form.validate()) {
            $form.disableForm();
            var data = $form.serializeObject();
            try{
                var res = $.rest.create('/staff/api/register', data);
                $form.enableForm();
                if(res.isOk){
                    window.location = '#!/main';
                    success('Your account has been registered');
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

    $('#login-form').submit(function(){
        try{
            var $form = $(this);
            $form.disableForm();

            var data = $form.serializeObject();

            var res = $.rest.create('/api/login', data);
            $form.enableForm();
            if(res.isOk){
                window.location='/staff';
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
//
//        var $form = $(this);
//        var data = $form.serializeObject();
//        $.ajax({
//            url:'/api/login',
//            type:'POST',
//            data : data,
//            dataType : 'json',
//            success : function(json){
//                if('ok' == json.result){
////                    location.reload();
//                    window.location='/';
//                }
//                if('validation' == json.result){
//                    var msg="";
//                    for (f in json.fields){
//                        $('[name="'+f+'"]', $form).addClass('error-field');
//                        msg += '<div>'+$('[name="'+f+'"]', $form).attr('placeholder')+': ' + json.fields[f][0]+'</div>';
//                    }
//                    $.error(msg);
//                } else if('error' == json.result){
//                    $.error(json.description);
//                }
//            }
//        });
        return false;
    });

    $('.otp-form').submit(function(){
        $(this).disableForm();
        try{
            var data = $(this).serializeObject();
            var res = $.rest.get('/api/checkotp', data);

            if(res.isOk){
                $('#staffRegisterForm').resetForm();
                $('input[name="yubiid"]', '#staffRegisterForm').val(data.otp.substring(0, 12));
                window.location = '#!/staff_register';
            } else {
                if (null == res.validationErrors){
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
    });

    $('#forgetForm').submit(function(){
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

});