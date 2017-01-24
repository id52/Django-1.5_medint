$.fn.serializeObject = function(){
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};


$(function(){
    $(document).on('keypress','.error',function(){
        $(this).prev('.error-alert').remove();
        $(this).removeClass('error');
    });
    $(document).on('change','.error',function(){
        $(this).prev('.error-alert').remove();
        $(this).removeClass('error');
    });
});



(function($){
    $.extend({
        success : function(str){
            $('.alert').html(str).removeClass('alert-error').addClass('alert-success').show().delay(6000).fadeOut('slow');
        },
        error : function(str){
            $('.alert').html(str).removeClass('alert-success').addClass('alert-error').show().delay(6000).fadeOut('slow');
        }
    })
})(jQuery);


(function($){
    var ifRequired = function(val){
        if ('undefined' === $.type(val)){
            return false;
        }
        if ('boolean' === $.type(val)){
            return val;
        }
        if ('string' === $.type(val)){
            return 'true' == val.toLowerCase() || 'yes' == val.toLowerCase();
        }
    };

    $.fn.validate = function(){
        var re;
        var errors = {}, err;
        var form = this;
//        $('input[type="text"], input[type="password"]', form).removeClass('error').removeAttr('title');
        this.each(function(){
            $.each($(this).find('input:text, input:password, select'), function(){
                var el = $(this);
                err = [];
//                el.change(function(){$(this).removeClass('error')});
                if (ifRequired(el.data('val-required'))){
                    if ('' === $.trim(el.val())){
                        el.val('');// if fields contains only spaces
                        err.push('This field is required')
                    }
                }
                if (el.data('val-regex') && 0 <$.trim(el.val()).length){
                    re = new RegExp(el.data('val-regex'));
                    if (!re.test($.trim(el.val()))){
                        err.push('This field is invalid');
                    }
                }
                if (el.data('val-equals')){
                    var sel = el.data('val-equals');
                    if($(sel, form).val() != el.val()){
                        err.push('Not equal to ' + $(sel).attr('placeholder'));
                    }
                }
                if(!$.isEmptyObject(err)){
                    errors[el.attr('name')]=err;
                }
            });
        });
        if(!$.isEmptyObject(errors)){
            this.showValidationErrors(errors);
            return false;
        }
        return true;
    };

    $.fn.showValidationErrors = function(options){
        function makeErrorDiv(error, explanation){
            return '<div class="error-alert"><div class="pointer"></div><div class="content"><p><strong>' + error +
                '</strong> ' + explanation + '</p></div><div class="ctright"></div></div>';
        }
        var form = this;
        form.each(function(){
            $.each(options, function(field, err){
                $('[name="' + field + '"]', form).addClass('error').before(makeErrorDiv(err[0], ''));
            });
        });
    };

    $.fn.resetForm = function(){
        $('input[type="text"], input[type="password"], select', this).val('').removeClass('error');
        $('.error-alert', this).remove();
    }
})(jQuery);


(function ($) {
    var response = function(resp){
        var status = resp.status;
        try{
            var res = $.parseJSON(resp.responseText);
            this.validationErrors = null;
            this.error = null;
            this.isOk = (199 < status) && (300 > status) && 'ok' == res.result;
            if (this.isOk ){
                this.data = res.data;
            } else if ('validation' == res.result){
                this.validationErrors = res.fields;
            } else {
                this.error = res.description;
            }
//            this.status = status;
        } catch (e){
            this.error = "Server error";
        }
        return this;
    }

    $.extend({
        rest:{
            auth : null,
            setAuth : function(auth){this.auth = auth;},
            get:function (url, data) {
                if (data){
                    var params = '', i;
                    for (i in data){
                        if (params.length > 0){
                            params += '&';
                        }
                        params += i + '=' + encodeURIComponent(data[i]);
                    }
                    url += '?' + params;
                }
                return this.perform("GET", 'GET', url, null);
            },
            create:function (url, data) {return this.perform("POST", 'POST', url, data);},
            update:function (url, data) {return this.perform("PUT", 'PUT', url, data);},
            remove:function (url, data) {return this.perform("DELETE", 'DELETE', url, data);},
            perform:function (method, overrideMethod, url, data) {
                var headers = { 'X-HTTP-Method-Override':overrideMethod };
                if (null !== this.auth){
                    headers['Authorization'] = 'Basic ' + this.auth;
                }
                var resp = $.ajax({
                    headers:headers,
                    dataType:"json",
                    url:url,
                    data:data,
                    type:method,
                    cache:false,
                    async:false
                });
//                console.log(resp);
                return new response(resp);
            }
        }
    });
})(jQuery);


(function($){
    $.fn.disableForm = function() {
        return this.each(function() {
            var form = $(this);
            var detachedHandlers = [];
            console.log("undefined" != typeof($._data(form[0], 'events')['submit']));
            if("undefined" != typeof($._data(form[0], 'events')['submit'])){
                $.each($._data(form[0], 'events')['submit'], function(){
                    detachedHandlers.push(this.handler);
                    form.off('submit', this.handler);
                });
            }
            form.data('detachedSubmit', detachedHandlers);
            form.on('submit', false);
            $('input[type="submit"]', form).attr('disabled','disabled');
            return form;
        });
    };

    $.fn.enableForm = function() {
        return this.each(function() {
            var form = $(this);
            if("undefined" != typeof($._data(form[0], 'events')['submit'])){
                $.each($._data(form[0], 'events')['submit'], function(){
                    form.off('submit', this.handler);
                });
            }
            $.each(form.data('detachedSubmit'), function(){
                form.on('submit', this);
            });
            $('input[type="submit"]', form).removeAttr('disabled');
            return form;
        });
    };

})(jQuery);


(function ($) {
    var stdAlert = window.alert;
    var defaultOpt = {
        tapToDismiss: true,
        extendedTimeOut: 1000,
        positionClass: 'toast-top-right',
        timeOut: 5000
    };

    window.alert = function(message) {
        if('undefined' !== typeof toastr){
            toastr.options = defaultOpt;
            toastr.warning(message, defaultOpt);
        } else {
            stdAlert(message);
        }
    };

    window.success = function(message) {
        if('undefined' !== typeof toastr){
            toastr.options = defaultOpt;
            toastr.success(message,defaultOpt);
        } else {
            stdAlert(message);
        }
    };

    window.error = function(message) {
        if('undefined' !== typeof toastr){
            toastr.options = defaultOpt;
            toastr.error(message, defaultOpt);
        } else {
            stdAlert(message);
        }
    };

    window.warning = function(message) {
        if('undefined' !== typeof toastr){
            toastr.options = defaultOpt;
            toastr.warning(message, defaultOpt);
        } else {
            stdAlert(message);
        }
    };

    window.info = function(message) {
        if('undefined' !== typeof toastr){
            toastr.options = defaultOpt;
            toastr.info(message, defaultOpt);
        } else {
            stdAlert(message);
        }
    };

    $.extend({
        ensure: function(text, callback){
            if ('undefined' !== typeof toastr){
                toastr.options = {
                    timeOut:0,
                    extendedTimeOut:0,
                    positionClass:'toast-top-full-width',
                    tapToDismiss:false,
                    messageClass: 'toast-confirm'
                }
                var msg = '<strong>Are you sure?</strong> '+text +
                     '<input type="button" value="Yes" id="toastrYes" class="btn btn-info"/>'+
                    '<input type="button" id="toastrNo" value="No" class="btn btn-danger" />';
                var t = toastr.notify ({iconClass: 'toast-confirm', message: msg, title: ''});
                t.delegate('#toastrYes', 'click', function () {
                    t.remove();
                    toastr.options = {}
                    toastr.clearImmediate();
                    callback();

                });
                t.delegate('#toastrNo', 'click', function () {
                    toastr.clear(t);
                });
            } else {
                if (confirm(text)){
                    callback();
                }
            }
        }
    })

})(jQuery);

