const uploadForm = document.getElementById('upload_form')
const inputFile = document.getElementById('id_video')
const progressBar = document.getElementById('progress')


$('#upload_form').submit(function (e) {
    e.preventDefault();
    $form = $(this);
    var formData = new FormData(this);
    const mediaData = inputFile.files[0];

    if (mediaData != null) {
        progressBar.classList.remove("not-visible");
    }

    $.ajax({
        type: 'POST',
        url: "/create/",
        data: formData,
        dataType: 'html',
        beforeSend: function () {

        },
        xhr: function () {
            const xhr = new window.XMLHttpRequest()
            xhr.upload.addEventListener('progress', e => {
                if (e.lengthComputable) {
                    const percentProgress = (e.loaded / e.total) * 100;
                    console.log(percentProgress)
                    progressBar.innerHTML = `<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="${percentProgress}" aria-valuemin="0" aria-valuemax="100" style="width: ${percentProgress}%"></div>`
                }
            })
            return xhr
        },
        success: function (response) {
            location.href = "../"
        },
        error: function (jqXHR, exception) {
            var msg = '';
            if (jqXHR.status === 0) {
                msg = 'Not connect.\n Verify Network.';
            } else if (jqXHR.status == 404) {
                msg = 'Requested page not found. [404]';
            } else if (jqXHR.status == 500) {
                msg = 'Internal Server Error [500].';
            } else if (exception === 'parsererror') {
                msg = 'Requested JSON parse failed.';
            } else if (exception === 'timeout') {
                msg = 'Time out error.';
            } else if (exception === 'abort') {
                msg = 'Ajax request aborted.';
            } else {
                msg = 'Uncaught Error.\n' + jqXHR.responseText;
            }
            console.log(msg)

        },

        cache: false,
        contentType: false,
        processData: false,
    })
})