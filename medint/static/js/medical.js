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

var background;
var position 	= {"home":0, "our-story":0.25, "who-we-are":0.5, "library":0.75, "talk-to-us":1};
var target="";
var oldtarget="";
var hash="";
var $topLoader;
var selectedBtn='#btn-directors';
var whoCat = '#directors';
var _heightW = $('#directors').height();
var error = false;
var msg="";
var inFP = false;
var HloginBox = 0;
var posLB;
var tablet=false;
var phone = false;

var getHash= function() {
    return location.hash.replace('#!/', '');
};


$(document).ready(function(e) {

	background 	= $('#background img');
	if( navigator.userAgent.match(/(iPad)|(android)|(webOS)|(tablet)/i) ){
		background.attr('src','/static/img/bkg_medical_tablet.jpg');
		tablet = true;
	}
	
	if( navigator.userAgent.match(/(iPhone)|(iPod)|(blackberry)|(smartphone)|(nexus one)|(htc)|(mobile_safari)/i)){
		$('#background').empty();
		
		$('body').css('background-color','#6fb1cd');
		$('div.copyright').empty();
		//$('body').css('background-attachment','fixed');
		//$('body').css('background-repeat','no-repeat');
		//$('body').css('background-size','768px 900px');
		//document.body.style.backgroundImage = 'url(/static/img/bkg_medical_mobile.jpg)';
		/*var nH = $('#library #l1').innerHeight();
		$('#library .container').css('height',nH) */
		phone = true;
		
	}
	$('#home,#our-story,#our-story .step2,#library,#who-we-are,footer,#talk-to-us').hide();
	$('#privacy,#bkgLogin').hide();
	$('#team,#advisors,.priv').hide();
	_width = document.body.clientWidth;
	_height = $(document).height();
	
	if(phone!=true){
                //$("#team #slide1").slides({container:'container',generateNextPrev: true});
				//$("#advisors #slide2").slides({container:'container',autoHeight:true,autoHeightSpeed:250,generateNextPrev: true});
				$("#library #slide").slides({autoHeight:true,container:'container',generateNextPrev: true});
	}

    var oldselectedManagement = "brazell";
    var olddselected = "brazell";
    var oldaselected = "johnson";

    $('#btn-brazell,#btn-dbrazell,#btn-ajohnson').addClass('active');

    //$('#aorrison .scroll-pane,#ajohnson .scroll-pane,#afiol .scroll-pane,#amann .scroll-pane').jScrollPane({});

    //$('#aorrison .scroll-pane,#ajohnson .scroll-pane,#afiol .scroll-pane,#amann .scroll-pane').mCustomScrollbar();

    function changeSectionAd(poldaselected){
        $("#btn-a"+oldaselected).removeClass('active');
        $('#a'+oldaselected).addClass('hidden');
        oldaselected = poldaselected;
        $('#a'+oldaselected).removeClass('hidden');
        //$('#a'+oldaselected+' .scroll-pane').jScrollPane();
    }

    $('#btn-ajohnson').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('johnson');
        return false;
    });

    $('#btn-alenert').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('lenert');
        return false;
    });

    $('#btn-aorrison').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('orrison');
        return false;
    });

    $('#btn-asengupta').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('sengupta');
        return false;
    });

    $('#btn-award').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('ward');
        return false;
    });

    $('#btn-afiol').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('fiol');
        return false;
    });

    $('#btn-amann').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('mann');
        return false;
    });

    $('#btn-aambati').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('ambati');
        return false;
    });

    $('#btn-apeiffer').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('peiffer');
        return false;
    });

    $('#btn-arowley').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('rowley');
        return false;
    });

    $('#btn-asundwall').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('sundwall');
        return false;
    });

    $('#btn-acochrane').on('click',function(){
        $(this).addClass('active');
        changeSectionAd('cochrane');
        return false;
    });



    $('#btn-dbrazell').on('click',function(){
        $("#btn-d"+olddselected).removeClass('active');
        $(this).addClass('active');
         $('#d'+olddselected).addClass('hidden');
        olddselected = "brazell";
        $('#d'+olddselected).removeClass('hidden');
        return false;
    });

    $('#btn-dkasten').on('click',function(){
        $("#btn-d"+olddselected).removeClass('active');
        $(this).addClass('active');
         $('#d'+olddselected).addClass('hidden');
        olddselected = "kasten";
        $('#d'+olddselected).removeClass('hidden');
        return false;
    });

    $('#btn-dweinstein').on('click',function(){
        $("#btn-d"+olddselected).removeClass('active');
        $(this).addClass('active');
        $('#d'+olddselected).addClass('hidden');
        olddselected = "weinstein";
        $('#d'+olddselected).removeClass('hidden');
        return false;

    });

    $('#btn-brazell').on('click',function(){
         $("#btn-"+oldselectedManagement).removeClass('active');
        $(this).addClass('active');
        $('#'+oldselectedManagement).addClass('hidden');
        oldselectedManagement = "brazell";
        $('#'+oldselectedManagement).removeClass('hidden');
        return false;

    });

    $('#btn-fields').on('click',function(){
         $("#btn-"+oldselectedManagement).removeClass('active');
        $(this).addClass('active');
        $('#'+oldselectedManagement).addClass('hidden');
        oldselectedManagement = "fields";
        $('#'+oldselectedManagement).removeClass('hidden');
        return false;

    });

    $('#btn-weinstein').on('click',function(){
         $("#btn-"+oldselectedManagement).removeClass('active');
        $(this).addClass('active');
        $('#'+oldselectedManagement).addClass('hidden');
        oldselectedManagement = "weinstein";
        $('#'+oldselectedManagement).removeClass('hidden');
        return false;

    });

    $('#btn-marbois').on('click',function(){
         $("#btn-"+oldselectedManagement).removeClass('active');
        $(this).addClass('active');
        $('#'+oldselectedManagement).addClass('hidden');
        oldselectedManagement = "marbois";
        $('#'+oldselectedManagement).removeClass('hidden');
        return false;

    });

    $('#btn-librett').on('click',function(){
         $("#btn-"+oldselectedManagement).removeClass('active');
        $(this).addClass('active');
        $('#'+oldselectedManagement).addClass('hidden');
        oldselectedManagement = "librett";
        $('#'+oldselectedManagement).removeClass('hidden');
        return false;

    });

    $('#btn-frenkel').on('click',function(){
        $("#btn-"+oldselectedManagement).removeClass('active');
        $(this).addClass('active');
        $('#'+oldselectedManagement).addClass('hidden');
        oldselectedManagement = "frenkel";
        $('#'+oldselectedManagement).removeClass('hidden');
        return false;

    });
	
	$(window).bind('hashchange', function(e) {
        hash = window.location.hash;
        target = hash.split('#!/');
        target = getHash();
        if(phone!=true) changeSection();
        else changeSectionMobile();
    });

	
	function positions(){
		var homeLeft = Math.round((_width*0.5)-($('#home').width()*0.5));
		$('#home,#our-story,#who-we-are,#library,#talk-to-us').css('left',homeLeft);
		if(_height > 800){
			$('#home').css('bottom','100px');
		}
		if(_width < 1200 && _height < 800){
			$('#home').css('bottom','60px');
		}
		
		if(_width < 767){
			$('#home').css('bottom','none');
		}
		
		if(_width < 1000) {$('footer #content').css('width','100%');$('footer .copyright').css('margin-right','10px');}
		else {$('footer #content').css('width',960);$('footer .copyright').css('margin-right','10px');}
		
		
	}

	background.css({bottom:0});
//	background.hide();
	
	if(phone!=true){
	if( $(window).width() < 1200 ) {background.attr('width',1200);if(tablet==true && $(window).width() < 959){background.attr('width','200%');}background.css({left:((_width)-background.width())*0.5});}
			else {background.attr('width','100%');background.css({left:0});}
		background.css({bottom:(($(window).height())-background.height())*position[target]});
	}
		
		
	
	if(phone!=true){ $("#menu").css('top',-100).show();positions();}
	else $("#menu").css('top',-400).show();
	
	

   
   function removeLoader(){
//		$('#loader').animate({top:0,opacity:0});
//		background.fadeIn(800);
		$("#menu").animate({top:0},800,'easeInOutQuad');
		$('footer').delay(900).fadeIn(600);
		$(window).trigger('hashchange');
	}
	
	setTimeout(removeLoader,600);

	
	$('#home-story').on('click',function(e){
		document.location='#!/our-story';
		return false;
		
	});
	
	$('#home-who').on('click',function(e){
		document.location='#!/who-we-are';
		return false;
		
	});
	
	$('.bt-readmore').on('mouseover',function(e){
		$(this).animate({left:'5px'},200);
		
	});
	
	$('.bt-readmore').on('mouseout',function(e){
		$(this).animate({left:'0'},200);
		
	});
	
	
	$('#btn-directors').on('click',function(e){
		$(selectedBtn).removeClass('active');
		$(this).addClass('active');
		selectedBtn = $(this);
		$(whoCat).fadeOut();
		whoCat = '#directors';
		$(whoCat).delay(1000).fadeIn();
		return false;
	});
	
	$('#btn-team').on('click',function(e){
		$(selectedBtn).removeClass('active');
		$(this).addClass('active');
		selectedBtn = $(this);
		$(whoCat).fadeOut();
		whoCat = '#team';
		//console.log("whoCat : "+whoCat);
		$(whoCat).delay(1000).fadeIn();
		return false;
	});
	
	$('#btn-advisors').on('click',function(e){
		$(selectedBtn).removeClass('active');
		$(this).addClass('active');
		selectedBtn = $(this);
		$(whoCat).fadeOut();
		whoCat = '#advisors';
		$(whoCat).delay(1000).fadeIn();
		return false;
	});
	
	
	$('footer #btn-privacy').on('click',function(e){
		scrollW = $('#scrolling').width();
		$('#scrolling').animate({left:-scrollW},1000,'easeInOutQuart');
		$('#menu,footer').animate({left:-scrollW},1000,'easeInOutQuart');
		$('#privacy').show(500);
		inFP = true;
		if(target=="login"){$('#login').hide();}
		return false;
	});
	
//	$('footer #btn-logout').live('click',function(e){
//		return false;
//
//	});
	
	$('#btn-priv').on('click',function(e){
		$(this).addClass('active');
		$('#btn-legal').removeClass('active');
		$('.legal').fadeOut();
		$('.priv').delay(1000).fadeIn();
		return false;
	});
	
	$('#btn-legal').on('click',function(e){
		$(this).addClass('active');
		$('#btn-priv').removeClass('active');
		$('.priv').fadeOut();
		$('.legal').delay(1000).fadeIn();
		return false;
	});
	
	$('#btn-back').on('click',function(e){
		inFP = false;
		$('#scrolling').animate({left:0},1000,'easeInOutQuart');
		$('#menu,footer').animate({left:0},1000,'easeInOutQuart');
		$('#privacy').delay(800).fadeOut(600);
		if(target=="login"){$('#login').delay(600).fadeIn(300);}
		return false;
	});
	
	$('#library a.more').on('click',function(e){
		return false;
		
	});

    $(document).on('submit', '#contactform', function(){
        var msg = '';
        if('' === $('[name="name"]', this).val()){
            msg+='Fill your name field\n';
        }
        var email = $('[name="email"]').val();
        if('' === email){
            msg+='Fill your email field\n';
        } else{
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            if(!re.test(email)){
                msg+=('Your email format is not correct. Please enter a valid email.');
            }
        }
        if('' === $('[name="text"]').val()){
            msg+='Fill your comments/message field\n';
        }

        if('' !== msg){
            alert(msg);
            return false;
        }
        $.ajax({
            url: '/api/feedback',
            type: 'POST',
            dataType: 'json',
            data: $(this).serializeObject(),
            success: function(json){
                if ('ok' == json.result){
                    alert('Your request has been accepted');
                    this.reset();
                } else if('validation' == json.result){
                    alert('Validation errors');
                } else {
                    alert('Internal error occurred. Please contact support')
                }

            }
        });

        return false;
    });
	
	
	
	function changeSection(){
		
		
		//background.animate({bottom:(($(window).height())-background.height())*position[target]}, 1000);
		//console.log("bkg height :"+background.height());
		
		background.animate({bottom:(($(window).height())-background.height())*position[target]}, 500, 'easeInOutQuart');
		
		$('#our-story .step2').delay(1000).fadeIn(300);
		//$('#our-story .step1').delay(1000).fadeIn(100);
		
		if(oldtarget!=""){
			$('#btn-'+oldtarget).removeClass('active');
		}
		$('#btn-'+target).addClass('active');
		
		if(target==""){
			target="home";
		}
		
		if(target=="login"){
			$('#login').delay(500).animate({top:posLB},600,'easeInOutQuart');
		}
		
		
		
		if(oldtarget!="" && oldtarget!="login") $('#'+oldtarget).fadeOut(400);
		if(oldtarget=="login"){$('#login').animate({top:-HloginBox-80},400,'easeInOutQuart');}
			//$('#'+target).delay(1800).fadeIn(600);
			$('#'+target).delay(1000).fadeIn(600);
			oldtarget = target;
		
		
	}
	
	function changeSectionMobile(){
		$('#our-story .step2').show();
		if(oldtarget!=""){
			$('#btn-'+oldtarget).removeClass('active');
		}
		$('#btn-'+target).addClass('active');
		
		if(target==""){
			target="home";
		}
		if(oldtarget!="" && oldtarget!="login") $('#'+oldtarget).fadeOut(400);
		$('#'+target).delay(1000).fadeIn(600);
		oldtarget = target;
	}
	
	
	

	/*if(phone == true){
		var nH = $('#library #l1').height()+$('#library #l2').height()+$('#library #l3').height();
		alert(nH);
		$('#library .container').css('height',nH) 
		
	}*/

	
	
	//background.css({bottom:(background.height()-($(window).height())*-position[target])});
		
	//background.css({bottom:(($(window).height())-background.height())*position[target]});
	
	
	
	
	
	$(window).resize(function(){
		if(phone!=true){
		_width = document.body.clientWidth;
		_height = $(document).height();
		scrollW = $('#scrolling').width();
		var alertW = Math.round(0.96*_width);
		if( $(window).width() < 1200 ) {background.attr('width',1200);if(tablet==true && $(window).width() < 959){background.attr('width','200%');}background.css({left:((_width)-background.width())*0.5}); }
			else {background.attr('width','100%');background.css({left:0});}
		background.css({bottom:(($(window).height())-background.height())*position[target]});
		positions();
		$('#loader').css('left',((_width/2)-80));
	}
	if(inFP == true){
			//console.log("dans INFP");
			$('#scrolling').css("left",-scrollW);
			$('#menu,footer').css("left",-scrollW-100);
		}
	
	});
});