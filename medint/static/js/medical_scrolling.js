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
var position 	= {"":0, "main":0, "login":0.9,"register":1};
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
	$('section#login,section#register,section#forget').hide();
	//$('#menu').hide();
	$('.bkg').hide();
	$('#logoP').hide();
	logoPW = $('#logoP').width();

    $(window).bind('hashchange', function(e) {
        console.log('hashchange');
        hash = window.location.hash;
        target = hash.split('#!/');
        target = getHash();
        console.log(target);
        changeSection();

    });
	
	if(!oldIE){
   $topLoader = $("#loader").percentageLoader({
      width: 140,
      height: 140,
      onProgressUpdate : function(val) {
         $topLoader.setValue(Math.round(val * 100.0));
      }
   });
   var topLoaderRunning = false;
   }
   
//    function running(){
//
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
   
//   function removeLoader(){
//		$('#loader').animate({top:-400,opacity:0});
//		//changeSection();
//		$(window).trigger('hashchange');
//		//changeSection();
//		//displayPanel();
//	}
	
//	if(!oldIE){
//
//		running();
//	}
//	else{/*displayPanel();*/changeSection();}
    changeSection();
	
	$('#loader').css('top',((_height/2)-80));
	$('#loader').css('left',((_width/2)-80));
	//$('#loginPanel').css('margin-top',((_height/2)-(logPanelH*0.5)));
	//target = "";
	//console.log($(window).height());
	
	$('#logoP,#logoF').live('click',function(e){
		window.location='#!/main';
	});
	
	

	
	
	function changeSection(){
		background.animate({bottom:(($(window).height())-background.height())*position[target]}, 1000, 'easeInOutQuart');
		oldtarget = target;
	}
	


	
	
	//background.css({bottom:(background.height()-($(window).height())*-position[target])});	
	background.css({bottom:(($(window).height())-background.height())*position[target]});
	
	
	
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
	
	
	$("input").each(function(){
			if($(this).val()=="" && $(this).attr("placeholder")!=""){
				$(this).val($(this).attr("placeholder"));
				$(this).focus(function(){
					if($(this).val()==$(this).attr("placeholder")) $(this).val("");
				});
				$(this).blur(function(){
					if($(this).val()=="") $(this).val($(this).attr("placeholder"));
				});
			}
		});
	
	$('#logo,#loginb,#who,footer').hide();
	$('.alert').hide();
	
	$('input#btn-sign').bind('click',function(){
		
		if (document.medicalSignup.EMAIL.value != "")	{
		indexAroba = document.medicalSignup.email.value.indexOf('@');
		indexPoint = document.medicalSignup.email.value.indexOf('.');
		if ((indexAroba < 0) || (indexPoint < 0))		{
			$('#alert-error').html("Your email format is not correct. Please enter a valid email.");
		$('#alert-error').show();
		$('#alert-success').hide();
		$('#alert-error').delay(6000).fadeOut('slow');
		}
		else{
			$('#alert-success').html("Your email has been added to our list. We will be notified soon !");
			$('#alert-success').show();
			$('#alert-error').hide();
			$('#alert-success').delay(6000).fadeOut('slow');
		}
	}
	
	else{
		$('#alert-error').html("Please enter a valid email.");
		$('#alert-error').show();
		$('#alert-success').hide();
		$('#alert-error').delay(6000).fadeOut('slow');
	}
		
		
		
	});
	
	//Login -> Go to website demo

	
	$('#main').css('top',_height-450);
	$('#logoP').css('left',((_width-logoPW)/2)-50);
	$('#logoP').css('top',80);
	topRegister = Math.round((_height*0.5)-($('#register').height()*0.5));
	topLogin = Math.round((_height*0.5)-($('#login').height()*0.5));
	$('#logoP').css('top',10);$('section#register').css('top',topRegister);
	$('section#login').css('top',topLogin);
	
	$('footer').css('position','absolute');
			$('footer').css('bottom',20);
			$('footer').css('left',footerL);
			$('footer').css('top','auto');
	
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
		if(_height>300 && _height<650){
		$('#main').css('top',40);
		$('footer').css('position','relative');
		$('footer').css('bottom',60);
		$('footer').css('left',0);
		$('section#login').css('top',130);
		$('section#register').css('top',120);
		$('#logoP').css('top',20);
		
	}
		
	
	if( $(window).width() < 1200 ) background.attr('width',1200);
			else background.attr('width','100%');
	
	
	/*$('#logo').delay(1000).show(600);
	$('#loginb').delay(1500).fadeIn("slow");
	$('#who').delay(2000).fadeIn('slow');
	$('footer').delay(3000).fadeIn('slow');
	$('.bkg').delay(2000).fadeIn('slow');*/
	
	
	
	
	$(window).resize(function(){
		_width = document.body.clientWidth;
		_height = $(document).height();
		footerL = (_width/2) - 220;
		var alertW = Math.round(0.96*_width);
		console.log("height :"+_height);
		
		
		if( $(window).width() < 1200 ) background.attr('width',1200);
			else background.attr('width','100%');
			background.css({bottom:(($(window).height())-background.height())*position[target]});
			/*if(target =="" || target!="main" || target !="login")*/
			/*if(target =="register") background.css({bottom:(($(window).height())-background.height())*position["login"]});*/
			/*if(target !="" && target!="main" && target !="login") background.css({bottom:(($(window).height())-background.height())*0});*/
		
		
	 	$('#main').css('top',_height-550);
		$('.alert').css('width',alertW);
		
		$('#logoP').css('left',((_width-logoPW)/2)-50);
		
		
		$('footer').css('position','absolute');
			$('footer').css('bottom',20);
			$('footer').css('left',footerL);
			$('footer').css('top','auto');
			
		topRegister = Math.round((_height*0.5)-($('#register').height()*0.5));
		topLogin = Math.round((_height*0.5)-($('#login').height()*0.5));
		if(target=="register") $('section#register').css('top',topRegister);
		if(target=="login") $('section#login').css('top',topLogin);
		
			
		if(_height>800){
			$('#main').css('top',200);
			$('footer').css('position','absolute');
			$('footer').css('bottom',20);
			$('footer').css('left',footerL);
			$('footer').css('top','auto');
			$('#logoP').css('top',80);
			$('section#register').css('top',topRegister);
			$('section#login').css('top',topLogin);
		}
		
		if(_height>=650 && _height<800){
			$('#main').css('top',120);
			$('section#login').css('top',150);
			$('section#register').css('top',140);
			$('#logoP').css('top',20);
			
		}
		if(_height>300 && _height<650){
			$('#main').css('top',40);
			$('footer').css('position','relative');
			$('footer').css('bottom',60);
			$('footer').css('left',0);
			$('section#login').css('top',130);
			$('section#register').css('top',120);
			$('#logoP').css('top',20);
		}
		
		
		
		
	
	});
	
	
	
	
});