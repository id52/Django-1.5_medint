
$.fn.extend({
    insertAtCaret: function(myValue){
      return this.each(function(i) {
        if (document.selection) {
          //For browsers like Internet Explorer
          this.focus();
          sel = document.selection.createRange();
          sel.text = myValue;
          this.focus();
        }
        else if (this.selectionStart || this.selectionStart == '0') {
          //For browsers like Firefox and Webkit based
          var startPos = this.selectionStart;
          var endPos = this.selectionEnd;
          var scrollTop = this.scrollTop;
          this.value = this.value.substring(0, startPos)+myValue+this.value.substring(endPos,this.value.length);
          this.focus();
          this.selectionStart = startPos + myValue.length;
          this.selectionEnd = startPos + myValue.length;
          this.scrollTop = scrollTop;
        } else {
          this.value += myValue;
          this.focus();
        }
      })
    },

    wrap: function(val){
        return this.each(function(i) {
            if (document.selection) {
                this.focus();
                var sel = document.selection.createRange();
                sel.text = val[0] + sel.text + val[1];
                this.focus();
            } else if (this.selectionStart || '0' == this.selectionStart) {
                var startPos = this.selectionStart;
                var endPos = this.selectionEnd;
                var content = this.value.substring(startPos, endPos);
                var scrollTop = this.scrollTop;
                this.value = this.value.substring(0, startPos)+val[0] + content + val[1] + this.value.substring(endPos,this.value.length);
                this.focus();
                this.selectionStart = startPos + val[0].length;
                this.selectionEnd = endPos + val[0].length;
                this.scrollTop = scrollTop;
            } else{
            }
        })
    }
});

$(function(){
    var editorForm = $('#disease-article');
    var currentDisease = null;

    $('#button-part').click(function(){
        $('#editor').wrap(['# ', '\n']);
        return false;
    });
    $('#button-strong').click(function(){
        $('#editor').wrap(['**', '**']);
        return false;
    });
    $('#button-em').click(function(){
        $('#editor').wrap(['_', '_']);
        return false;
    });
    $('#button-ol').click(function(){
        $('#editor').wrap(['* ', '\n']);
        return false;
    });
    $('#button-ul').click(function(){
        $('#editor').wrap(['1. ', '\n']);
        return false;
    });
    $('#button-preview').click(function(){
        $.ajax({
            url: '/wiki/api/preview',
            data: {'data': $('#editor').val()},
            dataType: 'html',
            type: 'POST',
            success: function(html){
                $('#preview-body').html(html);
                $('#button-save-popup').show();
                $('#box-preview').modal()
            }
        });
        return false;
    });

    var setState = function(state){
        $('li', '#article-toolbar').removeClass('active');
        var editArea = $('#edit-area').hide();
        var viewArea = $('#view-area').hide();
        var historyArea = $('#history-area').hide();

        if('view' == state){
            $('#btn-view').addClass('active');
            viewArea.show();
        }
        if('edit' == state){
            $('#btn-edit').addClass('active');
            editArea.show();
        }
        if('history' == state){
            $('#btn-history').addClass('active');
            historyArea.show();
        }
    };

    var onPreviewRevisionClick = function(){
        $.ajax({
            url: '/wiki/api/revision/' + $(this).parents('tr').data('id'),
            dataType: 'json',
            success: function(json){
                $('#button-save-popup').hide();
                $('#preview-body').html(json.data.html);
                $('#box-preview').modal();
            }
        });
    };

    var onUseClick = function(){
        $.ajax({
            url: '/wiki/api/article/' +currentDisease.id,
            data: {revision_id: $(this).parents('tr').data('id')},
            dataType: 'json',
            type: 'POST',
            success: function(json){
                setDisease(json.data);
                setState('view');
            }
        })
    };

    var deleteAttachment = function(){
        var id = $(this).parents('li').data('id');
        $.ajax({
            'url': '/wiki/api/image/' + id,
            type: 'DELETE',
            dataType: 'json',
            success: loadAttaches
        });
        return false
    };

    var showLicense = function(){
        $('#license-text').html($(this).parents('li').data('license'));
        $('#box-license').modal();
        return false;
    };

    var renderAttachments = function(attachments){
        var ul = $('#attachment-list').empty();
        $('#attachments-view').empty();
        for (var i=0; i<attachments.length; i++){
            var a = attachments[i];
            var li = $('<li />').data(a);
            var btn = $('<button class="btn"><span class="icon-trash"></span>Delete</button>').click(deleteAttachment);
            var license = a.license?$('<a href="#" class="license-handler">License</a>'):false;
            var div = $('<div class="attach-description"></div>')
                .append('<div>' + a.title + '</div>')
                .append(license?$('<div />').append(license):'');
            li.append($('<div class="thumbnail"></div>').css('background-image', 'url(' + a.url +')')).append(div);
            $('#attachments-view').append(li.clone().data(a));
            div.append(btn);
            ul.append(li);
        }
    };

    var setDisease = function(data){
        currentDisease = data;
        $('h1', '#view-area').text(data.title);
        $('#article').html(data.html);
        $('[name="name"]').val(data.title);
        $('[name="icd9"]').val(data.icd9);
        $('[name="data"]').val(data.data);
        $('[name="id"]').val(data.id);
        var history = $('tbody', '#history-area').empty();
        for (var i=0; i<data.revisions.length; i++){
            var rev = data.revisions[i];
            var tr = $('<tr>').data(rev);
            tr.append($('<td/>').text(rev.author));
            tr.append($('<td/>').text(rev.date));
            if(0 < i){
                var btnPreview = $('<button class="btn">').html('<span class="icon-eye-open"></span> Preview').click(onPreviewRevisionClick);
                var btnUse = $('<button class="btn">').html('<span class="icon-ok"></span> Use this').click(onUseClick);
                tr.append($('<td/>').append(btnPreview).append(btnUse));
            } else{
                tr.append($('<td>Current revision</td>'));
            }
            history.append(tr);
        }
        renderAttachments(data.attachments);
    };

    var onSearchResultClick = function(){
        $.ajax({
            url: '/wiki/api/disease/'+$(this).data('id'),
            dataType: 'json',
            success: function(json){
                setDisease(json.data);
                setState('view');
            }
        });
        return false;
    };

    var renderSearchResult = function (data){
        if (data && 0 < data.length){
            var ul=$('<ul />');
            for (var i=0; i<data.length; i++){
                var d = data[i];
                ul.append($('<li/>').append($('<a href="#" />').text(d.title).data(d).click(onSearchResultClick)));
            }
            $('#search-result').html(ul);
        } else {
            $('#search-result').html('Nothing found');
        }
        $('#search-result-wrapper').show();
    };

    var searchByICD9 = function(){
        $.ajax({
            url: '/wiki/api/search?q=' + $.trim($('#q').val()),
            dataType: 'json',
            success: function(json){
                if ('ok' == json.result){
                    renderSearchResult(json.data);
                }

            }
        });
        return false;
    };

    editorForm.submit(function(){
        var form = $(this);
        $.ajax({
            url: '/wiki/api/save',
            data: $(this).serializeObject(),
            dataType: 'json',
            type: 'POST',
            success: function(json){
                if ('ok' == json.result){
                    setDisease(json.data);
                    setState('view');
                }
            },
            error: function(e){
                console.log('ERROR');
                console.log(e);

            }
        });
        return false;
    });

    $('#search-button').click(searchByICD9);

    $('a','#btn-view').click(function(){
        setState('view');
        return false;
    });

    $('a', '#btn-edit').click(function(){
        setState('edit');
        return false;
    });

    $('a', '#btn-history').click(function(){
        setState('history');
        return false;
    });



    var uploadData = null;

    var loadAttaches = function(){
        $.ajax({
            url: '/wiki/api/image/' + currentDisease.id,
            dataType: 'json',
            success: function(json){
                console.log(json.data);
                renderAttachments(json.data);
            }
        });
    };

    $('#btn-upload-attach').click(function(){
        $('[name=articleid]','#form-upload-image').val(currentDisease.id);
        $('#box-upload-attach').modal();

        $('#form-upload-image').fileupload({
            url: '/wiki/api/image/',
            autoUpload: false,
            replaceFileInput: true,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            dataType: 'json',
            type: 'POST',
            add: function(e, data){
                uploadData = data;
                $('[name=fn]', '#form-upload-image').val(data.files[0].name);
                console.log(data.files[0].name);
            },
            success: function(json){
                $('#box-upload-attach').modal('hide');
                loadAttaches();
            }
        });
    });
    $('#form-upload-image').submit(function(){
        uploadData.articleid = currentDisease.id;
        uploadData.submit();
        return false;
    });
    $(document).on('click', '#button-save-popup', function(){
        return editorForm.submit();
    });

    $(document).on('click', '.license-handler', showLicense);

    $('#article').on('click', 'a', function(){
        $(this).attr('target', '_blank');
    });
});