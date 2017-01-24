var spinner;

function initMessages (sel){
    console.log('CREATE');



    var UPDATE_INTERVAL = 5000;
    ko.bindingHandlers.jScrollPane = {
        init: function(element, valueAccessor) {
//            var tmp = null;
//            if(0 < $('#uploader', element).length) {
//                tmp = $('#uploader').detach();
//            }
            var options = valueAccessor() || {
                verticalGutter: 12,
                verticalDragMinHeight: 54,
                autoReinitialise: false,
                animate: false
            };
//            //initialize
//            $(element).jScrollPane(options);
            var api = $(element).data('jsp');
            if (typeof api !== 'undefined') {
                api.reinitialise();
                api.scrollToY(api.getContentHeight());

            } else {
                api = $(element).jScrollPane(options).data('jsp');
                api.reinitialise();
                api.scrollToY(api.getContentHeight());
            }
//            if (null != tmp){
//                tmp.appendTo('.panel-column3 .uploader-wrapper');
//                tmp = null;
//            }
            //handle window resize
            $(window).resize(function() {
               var scroll = $(element).data("jsp");
               if (scroll) {
                  scroll.reinitialise();
               }
           });
        }
    };

    var baseUrl = '/api/messaging/discussion/';

    function Message (data) {
        this.id = ko.observable(data.id);
        this.text = ko.observable(data.text);
        this.subject = ko.observable(data.subject);
        this.files = data.files;

    }

    function Contact(info){
        var self = this;
        self.type = info.type;
        self.username = info.username;
        self.firstName = info.firstName;
        self.lastName = info.lastName;
        self.title = info.title;
        self.sent = info.sent;

        self.displayName = ko.computed(function(){
            if (self.firstName && self.lastName){
                return self.firstName + ' ' + self.lastName;
            }
            return self.username;
        });
    }


    function Discussion(info){

        var i, self = this;
        this.id = info.id;
        this.subject = info.subject;

        this.starter = new Contact(info.starter);
        this.members = [];

        self.messages = [];
        self.last_msg_time=info.last_msg_time;
        self.last_msg_date=info.last_msg_date;
        self.timeago=info.timeago;
        $("p.timeago").timeago();


        this.lastMessage = info.lastMessage;

        if ('undefined' !== typeof info.members){
            for (i=0; i<info.members.length; i++){
                this.members[i]=(new Contact(info.members[i]));
            }
        }

        if ('undefined' !== typeof info.messages){
            for (i=0; i<info.messages.length; i++){

                if(i==info.messages.length-1 && info.messages[i].editable)
                    info.messages[i].last=1;
                else
                    info.messages[i].last=0;

                info.messages[i].text = info.messages[i].text.replace(/\n/g, 'z<br>');
                self.messages.push(info.messages[i]);
            }
        }

        self.excerpt  = ko.computed(function(){
            return self.subject.length > 20 ?  self.subject.substring(0,30)+"..." : self.subject;
        });

        self.displayMembers = ko.computed(function(){
            var res = self.starter.displayName();
            for (i=0; i<self.members.length; i++){
                if(self.starter.displayName()!=self.members[i].displayName())
                    res += ', ' + self.members[i].displayName();
            }
            return res;
        });

        this.equals = function(x){
            if ('undefined' === typeof(x.id)){
                return false;
            }
            return x.id == this.id;
        }
    }


    function compareLastMessage(a, b){
        return b.lastMessage-a.lastMessage;
    };


    function MessageModel (){
        var self = this;
        self.folders = ko.observableArray([
            {title:'Inbox', folder: 'inbox', count: 0},
            {title:'Archives', folder: 'archive', count: 0},
            {title:'Trash', folder: 'trash', count: 0}
        ]);
        self.chosenFolder = ko.observable(self.folders()[0]);
        self.discussions = ko.observableArray([]);
        self.discussion = ko.observable(null);
        self.contacts = ko.observable([]);
        self.matchedContacts = ko.observable([]);
        self.recipients = ko.observable([]);
        self.uploadData = ko.observable(null);
        self.selectedFiles = ko.observableArray([]);

        var updateTimeout, list = [], fileMessageId = null;
        var source = new EventSource('/api/medint/updates/');

        var onMessage = function (event) {
            var d = $.parseJSON(event.data);
            var discussion = self.discussion();
            if (null != discussion && discussion.id == d.discussionId) {
                discussion.messages.push(d.message);
                self.discussion(new Discussion(discussion));
                fitSize();
                setTimeout(function(){
                    var api = $('#msglist').data('jsp');
                    api.reinitialise();
                    api.scrollToY(api.getContentHeight());
                }, 100);
                console.log('------------');
                console.log(self.discussion());
            }
//            console.log(d.discussionId);
//            console.log(d.message);
        };



        source.addEventListener("message", onMessage);
        source.addEventListener("error", function(e){
            console.error(e);
        });

        self.editMsg= function (m){
            $('.reply-area textarea').val(m['text']);
            var res = $.rest.remove('/api/messaging/message/'+ m.id);
            if(res.isOk){
                self.selectDiscussion(self.discussion());

            }
        };

        self.deleteMsg= function (m){
            var res = $.rest.remove('/api/messaging/message/'+ m.id);
            if(res.isOk){
                success('The message has been deleted');
                self.selectDiscussion(self.discussion());

            }
        };

        self.selectDiscussion = function (d) {
            function doSelect(){
                var res = $.rest.get(baseUrl  + d.id);
                if (res.isOk){
                    self.discussion(new Discussion(res.data));
                }
                res = null;
                fitSize();
                setTimeout(function(){
                    var api = $('#msglist').data('jsp');
                    api.reinitialise();
                    api.scrollToY(api.getContentHeight());
                }, 100);
            }

            if (null == fileMessageId){
                doSelect();
            } else {
                $.ensure('Your message with attachment will be submitted.', function(){
                    $('.reply-form form').submit();
                    fileMessageId = null;
                    self.selectedFiles.removeAll();
                    doSelect();
                });
            }
            $(".timeago").timeago();
              self.uploadData(null);
        };

        self.discussion.subscribe(function(){
            $(".timeago").timeago();
        });

        self.selectFolder = function (f) {
            var dd = [], res = $.rest.get(baseUrl, {folder: f.folder});
            if (res.isOk){
                if ('undefined' !== typeof(res.data)){
                    for (var i=0; i<res.data.length; i++){
                        dd.push(new Discussion(res.data[i]));
                    }
                }

                self.discussions(dd);
            }
            self.chosenFolder (f);
            self.discussion(null);

            //get first discussion in the folder.
            if (0 < dd.length){
                var res = $.rest.get(baseUrl  + dd[0].id);
                if (res.isOk){
                    self.selectDiscussion(new Discussion(res.data));
//                               self.discussion(new Discussion(res.data));


                    setTimeout(function(){
                        fitSize();
                        var api = $('#msglist').data('jsp');
                        api.reinitialise();
                        api.scrollToY(api.getContentHeight());
                    }, 100);
                }
            };
        };

        self.deleteMessage = function (m){
            var text = 'trash' != self.chosenFolder().folder ? 'Move discussion to trash' : 'Completly remove this discussion';
            var res = 'trash' != self.chosenFolder().folder ? 'The discussion has been moved to the trash.' : 'The discussion has been deleted';

            $.ensure(text, function(){
                $.rest.update(baseUrl  + m.id, {folder:'trash'});
                self.discussion(null);
                self.selectFolder(self.chosenFolder());
                alert(res);

            });

        };

        self.archiveMessage = function (m, f){
            $.ensure('Archive this discussion', function(){
                $.rest.update(baseUrl  + m.id, {folder:'archive'});
                self.discussion(null);
                self.selectFolder(self.chosenFolder());
                alert('The discussion has been archived.');
            });
        };

        self.recoverMessage = function (m, f){
            $.ensure('Return discussion to the inbox', function(){
                $.rest.update(baseUrl  + m.id, {folder:'inbox'});
                self.discussion(null);
                self.selectFolder(self.chosenFolder());
                alert('The discussion has been returned to the inbox.');
            });
        };

        self.addRecipient = function(r){
            var i;
            if(null == self.discussion()){
                var rcp = self.recipients();
                rcp.push(r);
                self.recipients(rcp);
                $('input#to').val("");
                $('input#to').select();
                self.hideMatches();
//                showComposer();
            } else {
                var add = true;
                var members = self.discussion().members
                for (i=0; i<members.length; i++){
                    //console.log(members[i].username);
                    if (members[i].username == r.username){
                        add = false;
                        break;
                    }
                }
                if(add){
                   var res = $.rest.create(baseUrl + self.discussion().id + '/members', {username: r.username});
                   if (res.isOk){
                       success(r.displayName()+' have been added to the discussion');
                       self.selectDiscussion(self.discussion());
                   }

               } else {
                    error(r.displayName()+' is already added to the discussion');
                }
            }
            $('#contacts').modal('hide');

        }

        self.removeRecipient = function(r){
            if(null == self.discussion()){
                var i, rcp = self.recipients();
                for (i=0; i<rcp.length; i++){
                    if (rcp[i].username == r.username){
                        rcp.splice(i, 1);
                        break;
                    }
                }
                self.recipients(rcp);
            }
            $('input#to').focus();
        }

        self.showMatches = function(e, el){
            var i, res=[], val= $.trim($(el.target).val().toLowerCase()), contacts = self.contacts();
            if (0 == val.length){
                self.matchedContacts([]);
                return;
            }
            var rcp = self.recipients();
            for (i=0; i<contacts.length; i++){

                if(0 ==contacts[i].firstName.toLowerCase().indexOf(val) || 0 ==contacts[i].lastName.toLowerCase().indexOf(val))
                {
                    if (-1 == $.inArray(contacts[i], rcp)){
                        res.push(contacts[i]);
                    }
                }
            }
            self.matchedContacts(res);

        }

        self.preventSubmit = function(form, evt){
            if(13 == evt.which){
                evt.stopPropagation();
                if (0 != self.matchedContacts().length){
                    self.addRecipient(self.matchedContacts()[0]);
                    self.hideMatches();
                    $(evt.target).val('');
                }
                return false;
            } else if (8 == evt.which && 0 == $(evt.target).val().length && 0 != self.recipients().length){
                var rcp = self.recipients();
                rcp.pop();
                self.recipients(rcp);
            }
            return true;
        }

        self.hideMatches = function(){
            self.matchedContacts([]);
        }

        self.openAddressBook = function(){
            $('#contacts h3#myModalLabel').html('My address book');
            $('#contacts').modal();
        }

        self.openInviteAddressBook = function(){
            $('#contacts h3#myModalLabel').html('Add people');
            $('#contacts').modal();
        }

        self.updateBadges = function(){
            function update(data){
                if ('undefined' === typeof data){
                    return;
                }
                var i, j, d, countMap = {};
                var discussions = self.discussions();

                var updateDiscussion = false, updated = false;
                for (i=0; i<self.folders.length; i++){
                    self.folders[i].count=0;
                }
                for (i=0; i<data.length; i++){
                    d = data[i];
                    if(null!=self.discussion() && d.discussion == self.discussion().id && 0 != d.count){
                        updateDiscussion = true;
                    }

                    if(!countMap[d.folder]){
                        countMap[d.folder]=0;
                    }
                    countMap[d.folder] += d.count;
                    for(j=0; j<discussions.length; j++){
                        if (discussions[j].id == d.discussion && (discussions[j].lastMessage != d.lastMessage || discussions[j].count != d.count)){
                            updated = true;
                            discussions[j].last_msg_time= d.last_msg_time;
                            discussions[j].last_msg_date= d.last_msg_date;
                            discussions[j].timeago= d.timeago;
                            discussions[j]=new Discussion(discussions[j]);
                            discussions[j].count = d.count;
                            discussions[j].lastMessage = d.lastMessage;
                            break;
                        }
                    }
                };
                if(updated){
                    self.discussions.sort(compareLastMessage);
                }
                $("p.timeago").timeago();

                if(updateDiscussion){
                    var res = $.rest.get(baseUrl  + self.discussion().id);
                    if (res.isOk){
                        self.discussion(new Discussion(res.data));
                        fitSize();
                        setTimeout(function(){
                            var api = $('#msglist').data('jsp');
                            api.reinitialise();
                            api.scrollToY(api.getContentHeight());
                        }, 100);
                    }
                    res = null;
                }
                var folders = self.folders();
                for (i=0; i<folders.length; i++){
                    self.folders.replace(folders[i], {title:folders[i].title, folder: folders[i].folder,
                        count:countMap[folders[i].folder]?countMap[folders[i].folder]:0});
                }

            }
            $.ajax({
                url: '/api/messaging/count',
                dataType: 'json',
                success: function(json){
                    if ('ok' == json.result){
                        update(json.data);
                    } else if(json.description === "User is not authenticated"){
                        window.location="/#!/login";
                    };
                    clearTimeout(updateTimeout);
//                    updateTimeout = setTimeout(self.updateBadges, UPDATE_INTERVAL);
                }
            });

//            var res = $.rest.get('/api/messaging/count');
//            if (res.isOk) {
//                update(res.data);
//            };
//
//            if(res.error=="User is not authenticated"){
//                window.location="/#!/login";
//            };





//            res = null;
//            clearTimeout(updateTimeout);
//            updateTimeout = setTimeout(self.updateBadges, UPDATE_INTERVAL);
//          $.getJSON('/api/messaging/count', update);
        };

        self.showSelector = function(el){
//            console.log(el);
        }

        function activateButtonReply(){
           $(".reply-form form input[type=submit]").removeAttr("disabled");
            $(".reply-form form input[type=submit]").attr("value", "Add your reply");
        }

        function activateButtonNewMessage(){
            $(".form-message input[type=submit]").removeAttr("disabled");
            $(".form-message input[type=submit]").attr("value", "Send");
        }

        function initFileUplod(){

            return;
            $('#uploader').fileupload('destroy');
            $('#uploader').fileupload({
                url: '/api/messaging/attach/',
                filesContainer: '#files-list',
                dataType: 'json',
                autoUpload: true
            })
            .bind('fileuploadadd', function (e, data) {
                if (null === fileMessageId){
                    fileMessageId=new Date().getTime();
                }
                for (var i=0; i<data.files.length; i++){
                    self.selectedFiles.push(data.files[i].name);
                }
                $('#uploader').fileupload('option', 'formData', [{name: 'filemessageid', value: fileMessageId}]);
            });
            self.selectedFiles.removeAll();

        }

        function showComposer(){
            function doShow(){
                var tmp = $('#uploader').detach();
                self.discussion(null);
                $('.message-compose').removeClass('hide');
                tmp.appendTo('.message-compose .uploader-wrapper');
                tmp = null;
                $('.panel-column3 .uploader-wrapper').empty();
                $('.panel-column2,.panel-column3').addClass('hide');
                fileMessageId = null;
                self.selectedFiles.removeAll();
//                initFileUplod();
            }
            if (null == fileMessageId){
                doShow();
            } else {
                $.ensure('Your message with attachment will be submitted.', function(){
                    $('.reply-form form').submit();
                    fileMessageId = null;
                    self.selectedFiles.removeAll();
                    doShow();
                });
            }
        }

        function hideComposer(){
            self.recipients([]);
            $('.message-compose').addClass('hide');
            var tmp = $('#uploader').detach();
            $('.message-compose form').get(0).reset();
            $('.panel-column2,.panel-column3').removeClass('hide');
            tmp.appendTo('.panel-column3 .uploader-wrapper');
            tmp = null;

//            initFileUplod();
            fileMessageId = null;
            self.selectedFiles.removeAll();
            $('.message-compose .uploader-wrapper').empty();

        }

        $('.reply-form form').submit(function(){
            $(".reply-form form input[type=submit]").attr("value", "Please wait...");
            $(".reply-form form input[type=submit]").attr("disabled","disabled");
            var i, files = null;

            if(0 == $.trim($('textarea', this)).length && null == fileMessageId){
                error('Please enter some message content before hitting send!');
                return false;
            }

            var text = $('textarea', this).val();
            var spin = createSpinner('#reply-area form .spinner');
            spin.show();
            var data = {text: text};
            if(null != fileMessageId){
                data.filemessageid = fileMessageId;
            }
            var res = $.rest.create(baseUrl + self.discussion().id, data);
            if(res.isOk){
                spin.delay(300).fadeOut('fast',function(){$('#reply-area form .spinner').empty()});
                if (updateTimeout){
                    clearTimeout(updateTimeout);
                }
//                updateTimeout = self.updateBadges();
                $('textarea', this).val('');
                fileMessageId = null;
                self.selectedFiles.removeAll();

                //$("p.timeago").timeago();
                setTimeout(activateButtonReply,300);

            } else {
                error(res.error);
                setTimeout(activateButtonReply,300);
            }
            return false;
        });

        $('.form-message form').submit(function() {
            $(".form-message input[type=submit]").attr("disabled","disabled");
            $(".form-message form input[type=submit]").attr("value", "Please wait..");
            if(0 == $.trim($('[name="subject"]').val()).length){
                error('Please enter a subject!');
                setTimeout(activateButtonNewMessage,300);
                return false;
            }
            if(0 == $.trim($('[name="text"]').val()).length){
                error('Please enter a subject and some message content before hitting send!');
                setTimeout(activateButtonNewMessage,300);
                return false;
            }


            var i, members = [], rcp = self.recipients();
            if(0 == rcp.length){
                error('Please add at least one recipient!');
                setTimeout(activateButtonNewMessage,300);
                return false;
            }

            var spin = createSpinner('.form-message .spinner');
            spin.show();


//            var data = $(this).serializeArray();
            var data = {text: $('[name="text"]').val(), subject:$('[name="subject"]').val()};
            if(null != fileMessageId){
                data.filemessageid=fileMessageId;
            }
            var members=[];
            for (i=0; i<rcp.length; i++){
                members.push(rcp[i].username);
            }
            data['members[]'] = members;

            var res = $.rest.create(baseUrl, data);
            if (res.isOk){
                fileMessageId = null;
                self.selectedFiles.removeAll();
                spin.delay(300).fadeOut('fast',function(){$('.form-message .spinner').empty()});
                setTimeout(activateButtonNewMessage,300);
                this.reset();
                hideComposer();
                spin.hide();

                self.selectFolder(self.folders()[0]);
                self.selectDiscussion(self.discussions()[0]);

            } else {
                error(res.error);
            }
            return false;
        });

        (function(){
            createScroller('.panel-column2 .message-list .content');
            self.selectFolder(self.chosenFolder());
            var res = $.rest.get('/api/messaging/contact/');
            var i, c = [];
            if(res.isOk && res.data){
                for (i=0; i<res.data.length; i++){
                    c.push(new Contact(res.data[i]));
                }
                self.contacts(c);
            }
//            updateTimeout = self.updateBadges();

                initFileUplod();


            $('#uploader').fileupload({
                url: '/api/messaging/attach/',
                filesContainer: '#files-list',
                dataType: 'json',
                autoUpload: true,
                dropZone:'#message'
            })
            .bind('fileuploadadd', function (e, data) {
                if (null === fileMessageId){
                    fileMessageId=new Date().getTime();
                }
                for (var i=0; i<data.files.length; i++){
                    self.selectedFiles.push(data.files[i].name);
                }
                $('#uploader').fileupload('option', 'formData', [{name: 'filemessageid', value: fileMessageId}]);
            });



//            setInterval(self.updateBadges,UPDATE_INTERVAL);
            $('#btn-message-write').click(showComposer);
            $('#btn-cancel-message').click(hideComposer);
        })();
    }


    function fitSize(){
        var _w= $(window).width();
        var _h = $(window).height();
        var realp1;
        function f (){
            //var h = $('#msglist').parent().height();
            var h = Math.round(_h -55);
//            console.log('h=%s, height=%s', h, $('#msglist').height());
            //var hm =$('.panel-column3 .head-message').height() - 52;
            $('#msglist').height((h-335) + 'px');
//            $('.panel-column3 #msglist').height(h-160);
            var h2=$('.panel-column1').height()-290;
            $('.composer textarea').css('height',h2);

        }
        if($('.panel-column1').width() == 13){$('.panel-column2').width(0.13*_w)}
        clearTimeout(timer);
        timer = setTimeout(f, 100);
        if ($('.panel-column2').width() == 20){$('.panel-column2').width(0.2*_w)}
        var l= Math.round($('.panel-column1').width() +$('.panel-column2').width());
       if(l<300){/*$('.panel-column3').css('margin-left','33%');*/var nw=Math.round(300+(0.13*_w));$('.panel-column3').css('margin-left',nw);}
        else{$('.panel-column3').css('margin-left',l);}


    }
    var timer;
    setTimeout(fitSize, 400);

    function createScroller(ptarget){
        var pane = $(ptarget);
        pane.jScrollPane({
            verticalGutter: 12,
            verticalDragMinHeight: 54,
            autoReinitialise: true,
            animate: true
        });
        return pane.data('jsp');
    }
    $(window).resize(fitSize);

    ko.applyBindings(new MessageModel(), $(sel)[0]);



    function createSpinner(ptarget){
        var opts={
            lines: 7, // The number of lines to draw
            length: 0, // The length of each line
            width: 3, // The line thickness
            radius: 5, // The radius of the inner circle
            corners: 1, // Corner roundness (0..1)
            rotate: 9, // The rotation offset
            direction: 1, // 1: clockwise, -1: counterclockwise
            color: '#fff', // #rgb or #rrggbb
            speed: 1, // Rounds per second
            trail: 36, // Afterglow percentage
            shadow: false, // Whether to render a shadow
            hwaccel: false, // Whether to use hardware acceleration
            className: 'spinners', // The CSS class to assign to the spinner
            zIndex: 2e9, // The z-index (defaults to 2000000000)
            top: 'auto', // Top position relative to parent in px
            left: 'auto' // Left position relative to parent in px
        }

        var target= $(ptarget);
        spinner = new Spinner(opts).spin();
        return target.append(spinner.el);

    };

    $("p.timeago").timeago();

}

