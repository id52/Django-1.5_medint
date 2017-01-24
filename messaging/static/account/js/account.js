var oldAccountView;
oldAccountView ="personal-settings";

function accountModelView(){
    var self = this;
    self.userphone = ko.observable("(124) 555-0124");
    self.usercity = ko.observable("Los Angeles");
    self.userzipcode = ko.observable("CA");
    self.useraddress = ko.observable("1 place Massena");
    self.userstate = ko.observable("CA");
    self.userpwd = ko.observable("1234567");

}
ko.applyBindings(new accountModelView(), $('#accounts .settings-col')[0]);

$("#btn-password-settings").on('click',function(e){
    $("."+oldAccountView).addClass('hidden');
    $("#btn-"+oldAccountView).parent().removeClass("active");
    $(".password-settings").removeClass('hidden');
    oldAccountView = "password-settings";
    $(this).parent().addClass("active");

});

$("#btn-personal-settings").on('click',function(e){
    $("."+oldAccountView).addClass('hidden');
    $("#btn-"+oldAccountView).parent().removeClass("active");
    $(".personal-settings").removeClass('hidden');
    oldAccountView = "personal-settings";
    $(this).parent().addClass("active");

});

$("#btn-notifications-settings").on('click',function(e){
    $("."+oldAccountView).addClass('hidden');
    $("#btn-"+oldAccountView).parent().removeClass("active");
    $(".notifications-settings").removeClass('hidden');
    oldAccountView = "notifications-settings";
    $(this).parent().addClass("active");

});

