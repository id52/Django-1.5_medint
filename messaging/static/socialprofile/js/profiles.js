var currentprofileSection = "activities";
$("ul.navprofile li#btn-"+currentprofileSection).addClass("active");


$("ul.navprofile li#btn-bio").on('click',function(){
    $(this).addClass("active");
    $('#'+currentprofileSection).addClass("hidden");
    $("ul.navprofile li#btn-"+currentprofileSection).removeClass("active");
    currentprofileSection = "bio";
     $('#'+currentprofileSection).removeClass("hidden");
    return false;
});

$("ul.navprofile li#btn-activities").on('click',function(){
    $(this).addClass("active");
    $("ul.navprofile li#btn-"+currentprofileSection).removeClass("active");
    $('#'+currentprofileSection).addClass("hidden");
    currentprofileSection = "activities";
    $('#'+currentprofileSection).removeClass("hidden");
    return false;
});

$('.new-post textarea').on('focus',function(e){
    $('.new-post .clearfix').removeClass('hidden');
});

$('#wrapper').scroll(function(){
    var scrolling = $('#wrapper').scrollTop();
    if(scrolling >= 280){
       // $('.headerwrap').removeClass('hidden');
        $('.headerwrap').animate({top:'53px'}, 200);
        //$('.headerwrap').css('top',53);
    }
    else{
        $('.headerwrap').animate({top:'0'}, 200);
    }
});

$('.profilePicThumb').on('mouseover',function(e){
   $('.btn-edit-Thumb').show();
});

$('.profilePicThumb').on('mouseout',function(e){
   $('.btn-edit-Thumb').hide();
});

$('.cover').on('mouseover',function(e){
   $('.btn-cover').show();
});

$('.cover').on('mouseout',function(e){
   $('.btn-cover').hide();
});

$('.btn-cover,.btn-header-cover').on('click',function(){
    $('#update-cover').modal();
});

$('.btn-edit-Thumb,.btn-header-profile').on('click',function(){
    $('#update-thumb').modal();
});