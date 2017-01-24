// JavaScript Document
var _height;
var _width;
var footerL;
var i=1;
var angle=0;
var delay;
var ray;
var cnv;
var cnv2;
var oldIE = $.browser.msie && $.browser.version <= 8;
var background;
var position 	= {"":0, "main":0, "login":0.8,"register":0.8};
var target="";
var hash="";
var $topLoader;
var oldtarget="";
var logoPW;
var topRegister;
var topLogin;



var getHash= function() {
		return location.hash.replace('#!/', '');
	}
	
	
	
$(document).ready(function(e) {
	background 	= $('#background img');
	_width = document.body.clientWidth;
	_height = $(window).height();
	footerL = (_width/2) - 220;
    $('footer').css('left',footerL);
	background.css('bottom',0);
	
	$('.bkg').hide();
	$('#logoP').hide();
	$('#logo,#loginb,#who,footer,#login,#register').hide();
	$('.alert').hide();
	logoPW = $('#logoP').width();
	
//	if(!oldIE){
//   		$topLoader = $("#loader").percentageLoader({width: 140,height: 140,
//      	onProgressUpdate : function(val) {
//         	$topLoader.setValue(Math.round(val * 100.0));
//      	}
//   		});
//   		var topLoaderRunning = false;
//    }

    $(window).bind('hashchange', function(e) {
        hash = window.location.hash;
        target = hash.split('#!/');
        target = getHash();
        console.log(target);
        changeSection();

    });
   
//   function running(){
//       removeLoader();
//       return;
//	   if (topLoaderRunning) {
//         return;
//      }
//      topLoaderRunning = true;
//      $topLoader.setProgress(0);
//      $topLoader.setValue('0kb');
//      var kb = 0;
//      var totalKb = 500;
//
//      var animateFunc = function() {
//         kb += 10;
//         $topLoader.setProgress(kb / totalKb);
//         $topLoader.setValue(kb.toString() + 'kb');
//
//         if (kb < totalKb) {
//            setTimeout(animateFunc, 25);
//         } else {
//            topLoaderRunning = false;
//			removeLoader();
//         }
//      }
//      setTimeout(animateFunc, 25);
//
//   }
   
   function removeLoader(){
		$('#loader').animate({top:-400,opacity:0});
		$(window).trigger('hashchange');
	}  
	
//	if(!oldIE){
//		running();
//	}
//	else{
//        changeSection();
//    }
    changeSection();
//
	$('#loader').css('top',((_height/2)-80));
	$('#loader').css('left',((_width/2)-80));
	

	
	function callLoginForm(){
//		$("#ctPanel").empty();
//		$.ajax({
//			url:"/static/include/login.html",
//			success:function(data){
//				$('#ctPanel').html(data);
//			}
//			});
		return false;
	}
	
	if( $(window).width() < 1200 ){background.attr('width',1200);background.css({left:((_width+50)-background.width())*0.5});}
	else background.attr('width','100%');
	
	function changeSection(){
		background.animate({bottom:(($(window).height())-background.height())*position[target]}, 1000, 'easeInOutQuart');

		if(target=="main" || target==""){
			$('#logoP').hide();
			$('#logo').delay(1000).show(600);
			$('#loginb').delay(1500).fadeIn(600);
			$('#who').delay(2200).fadeIn('slow');
			$('footer').delay(2500).fadeIn('slow');
			$('.bkg').delay(2000).fadeIn('slow');
			if(oldtarget !="" && oldtarget!="main"){
				$('#'+oldtarget).fadeOut('slow');
			}
		}
		
		if(target=="login"){
			$('#logo').fadeOut("fast");
			$('#loginb').fadeOut("fast");
			$('#who').fadeOut('fast');
			$('footer').fadeOut('fast');
			$('#logoP').delay(800).fadeIn(200);
			$('.bkg').fadeOut('fast');	
			if(oldtarget !="" && oldtarget!="main"){
				$('#'+oldtarget).fadeOut('slow');
			}
			$('#'+target).delay(500).fadeIn('slow');
			setTimeout(callLoginForm,500);
			
		}
		
		if(target=="register"){
			$('#logo').fadeOut("fast");
			$('#logoP').fadeOut("fast");
			$('#loginb').fadeOut("fast");
			$('#who').fadeOut('fast');
			$('footer').fadeIn('fast');
			$('#login').fadeOut('slow');
			$('.bkg').fadeOut('fast');
			$('#logoP').delay(800).fadeIn(200);
			if(oldtarget !="" && oldtarget!="main"){
				$('#'+oldtarget).fadeOut('slow');
			}
			$('#'+target).delay(500).fadeIn('slow');
			
		}
		oldtarget = target;
	}
	
	$('#logoP,#logoF').live('click',function(e){
		window.location='#!/main';
	});
	
//	$('input#btn-sign').bind('click',function(){
//
//		if (document.medicalSignup.email.value != "")	{
//		indexAroba = document.medicalSignup.email.value.indexOf('@');
//		indexPoint = document.medicalSignup.email.value.indexOf('.');
//		if ((indexAroba < 0) || (indexPoint < 0))		{
//			$('#alert-error').html("<p>Your email format is not correct. Please enter a valid email.</p>");
//		$('#alert-error').show();
//		$('#alert-success').hide();
//		$('#alert-error').delay(6000).fadeOut('slow');
//		}
//		else{
//			$('#alert-success').html("<p>Your email has been added to our list. We will be notified soon !</p>");
//			$('#alert-success').show();
//			$('#alert-error').hide();
//			$('#alert-success').delay(6000).fadeOut('slow');
//		}
//	}
//
//	else{
//		$('#alert-error').html("Please enter a valid email.");
//		$('#alert-error').show();
//		$('#alert-success').hide();
//		$('#alert-error').delay(6000).fadeOut('slow');
//	}
//
//
//
//	});
	
	//Login -> Go to website demo
	$('input#btn-login').bind('click',function(){
		window.location= "demo/";
		return false;
	});
	
	
	function positions(){
		var alertW = Math.round(0.955*_width);
		$('#main').css('top',_height-450);
		$('footer').css('position','absolute');
		$('footer').css('bottom',20);
		$('footer').css('left',footerL);
		$('footer').css('top','auto');
		$('#logoP').css('left',((_width-logoPW)/2)-50);
		
		if(_height>300 && _height<650){
			$('#main').css('top',40);
			$('footer').css('position','relative');
			$('footer').css('bottom',60);
			$('footer').css('left',0);
			$('section#login').css('top',130);
			$('section#register').css('top',120);
			$('#logoP').css('top',20);
		
		}
		
		if(_height>800){
			$('#main').css('top',200);
			$('footer').css('position','absolute');
			$('footer').css('bottom',20);
			$('footer').css('left',footerL);
			$('footer').css('top','auto');
		}
		
		if(_height>=650 && _height<800){
			$('#main').css('top',120);
			$('section#login').css('top',150);
			$('section#register').css('top',140);
			$('#logoP').css('top',20);
			
		}
		
		
	}
	
	positions();
	
	$('#btn-forget').live('click',function(e){
		$("#ctPanel").empty();
		$.ajax({
			url:"/static/include/forget.html",
			success:function(data){
				$('#ctPanel').html(data);
			}
			});
		return false;
		
	});
	
	
//	$('#btn-login').live('click',function(e){
//		$("#ctPanel").empty();
//		$.ajax({
//			url:"/static/include/login.html",
//			success:function(data){
//				$('#ctPanel').html(data);
//			}
//			});
//		return false;
//
//	});
	
	if(oldIE){
		$("input#email").val("Your e-mail address");
		
		if($("input#email").val()=="Your e-mail address"){
		$("input#email").focus(function(){
			if($(this).val()=="Your e-mail address") $(this).val("");
		});
		$("input#email").blur(function(){
			if($(this).val()=="") $(this).val("Your e-mail address");
		});
		}
	}
	
	
//	$("input").each(function(){
//			if($(this).val()=="" && $(this).attr("placeholder")!=""){
//				$(this).val($(this).attr("placeholder"));
//				$(this).focus(function(){
//					if($(this).val()==$(this).attr("placeholder")) $(this).val("");
//				});
//				$(this).blur(function(){
//					if($(this).val()=="") $(this).val($(this).attr("placeholder"));
//				});
//			}
//		});
	
	
	
	$(window).resize(function(){
		console.log('target :'+target);
		_width = document.body.clientWidth;
		_height = $(document).height();
		
		footerL = (_width/2) - 220;
		positions();
		
		bottomBkg = Math.round((($(window).height()+50)-background.height())*position[target]);
		
		if( $(window).width() < 1200 ){background.attr('width',1200);background.css({left:((_width)-background.width())*0.5});}
			else{background.attr('width','100%');background.css({left:0});}
		background.css('bottom',bottomBkg);
		
	});
	
	
});