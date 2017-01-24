function sendFormCover()
{
    var loadImg=document.getElementById('loadImgCover');
    loadImg.style.visibility='visible';
    if(typeof files !== 'undefined')
        sendfilesCover(files);
    else
        document.forms['form_update_cover'].submit();

};



var holder = document.getElementById('dropzone_cover'),
    tests =
    {
      filereader: typeof FileReader != 'undefined',
      dnd: 'draggable' in document.createElement('span'),
      formdata: !!window.FormData,
      progress: "upload" in new XMLHttpRequest
    },
    support =
    {
      filereader: document.getElementById('filereader_cover'),
      formdata: document.getElementById('formdata_cover')
    },
    acceptedTypes =
    {
      'image/png': true,
      'image/jpeg': true,
      'image/gif': true
    },

    fileupload = document.getElementById('upload_cover');



function previewfileCover(file)
{

  console.log('function previewfile()');
  if (tests.filereader === true && acceptedTypes[file.type] === true)
  {
    var reader = new FileReader();
    reader.onload = function (event)
    {
        var img=document.getElementById('img_cover');
        img.src=event.target.result;

        var img=document.getElementById('select_file_cover');
        img.style.visibility='hidden';

    };

    reader.readAsDataURL(file);
  }

};




function sendfilesCover(files)
{
    console.log('function sendfiles()');
    var formData = tests.formdata ? new FormData() : null;

    for (var i = 0; i < files.length; i++)
    {
      if (tests.formdata) formData.append('cover', files[i]);
      previewfileCover(files[i]);
    }

    if (tests.formdata)
    {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/doctor/uploadPhoto');
      xhr.send(formData);
      xhr.onload=function foo()
      {
              //var getCover=document.getElementById('getCover');
              //getCover.src="/doctor/getCover?r="+Math.random();
              var loadImg=document.getElementById('loadImgCover');
              loadImg.style.visibility='hidden';
              window.location.reload();



      };

    };



};





function readfilesCover(files)
{
    console.log('function readfiles()');
    var formData = tests.formdata ? new FormData() : null;
    for (var i = 0; i < files.length; i++)
    {
      if (tests.formdata) formData.append('cover', files[i]);
      previewfileCover(files[i]);
    }
};




if (tests.dnd)
{

  holder.ondragover = function () {  return false; };
  holder.ondragend = function () {  return false; };
  holder.ondrop = function (e)
  {
    e.preventDefault();
    readfilesCover(e.dataTransfer.files);

    files= e.dataTransfer.files;



  }

}
else
{

  fileupload.querySelector('input').onchange = function ()
  {
    readfilesCover(this.files);
  };
}











//////////////////////////////////////////////////////////////












function sendFormPhoto()
{
    var loadImg=document.getElementById('loadImgPhoto');
    loadImg.style.visibility='visible';
    if(typeof files !== 'undefined')
        sendfilesPhoto(files);
    else
        document.forms['form_update_photo'].submit();

};



var holder = document.getElementById('dropzone_photo'),
    tests =
    {
      filereader: typeof FileReader != 'undefined',
      dnd: 'draggable' in document.createElement('span'),
      formdata: !!window.FormData,
      progress: "upload" in new XMLHttpRequest
    },
    support =
    {
      filereader: document.getElementById('filereader_photo'),
      formdata: document.getElementById('formdata_photo')
    },
    acceptedTypes =
    {
      'image/png': true,
      'image/jpeg': true,
      'image/gif': true
    },

    fileupload = document.getElementById('upload_photo');



function previewfilePhoto(file)
{

  console.log('function previewfile()');
  if (tests.filereader === true && acceptedTypes[file.type] === true)
  {
    var reader = new FileReader();
    reader.onload = function (event)
    {
        var img=document.getElementById('img_photo');
        img.src=event.target.result;

        var img=document.getElementById('select_file_photo');
        img.style.visibility='hidden';

    };

    reader.readAsDataURL(file);
  }

};




function sendfilesPhoto(files)
{
    console.log('function sendfiles()');
    var formData = tests.formdata ? new FormData() : null;

    for (var i = 0; i < files.length; i++)
    {
      if (tests.formdata) formData.append('photo', files[i]);
      previewfilePhoto(files[i]);
    }

    if (tests.formdata)
    {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/doctor/uploadPhoto');
      xhr.send(formData);
      xhr.onload=function foo()
      {
              //var getPhoto=document.getElementById('getPhoto');
              //getPhoto.src="/doctor/getPhoto?r="+Math.random();
              var loadImg=document.getElementById('loadImgPhoto');
              loadImg.style.visibility='hidden';
              window.location.reload();



      };

    };



};





function readfilesPhoto(files)
{
    console.log('function readfiles()');
    var formData = tests.formdata ? new FormData() : null;
    for (var i = 0; i < files.length; i++)
    {
      if (tests.formdata) formData.append('photo', files[i]);
      previewfilePhoto(files[i]);
    }
};




if (tests.dnd)
{

  holder.ondragover = function () {  return false; };
  holder.ondragend = function () {  return false; };
  holder.ondrop = function (e)
  {
    e.preventDefault();
    readfilesPhoto(e.dataTransfer.files);

    files= e.dataTransfer.files;



  }

}
else
{

  fileupload.querySelector('input').onchange = function ()
  {
    readfilesPhoto(this.files);
  };
}

