document.addEventListener('DOMContentLoaded', function() {
    var dropArea = document.getElementById('drop-area');
    var fileElem = document.getElementById('fileElem');
    var previewArea = document.getElementById('preview-area');
    var form = document.querySelector('form');
    var progressBar = document.getElementById('progress-bar');
    var progressBarContainer = document.getElementById('progress-bar-container');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropArea.classList.add('highlight');
    }

    function unhighlight(e) {
        dropArea.classList.remove('highlight');
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        var dt = e.dataTransfer;
        var files = dt.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        fileElem.files = files;
        previewFiles(files);
        dropArea.style.display = 'none'; // скрываем область загрузки
    }

    function showDropAreaIfEmpty() {
        if (fileElem.files.length === 0) {
            dropArea.style.display = 'block';
            document.querySelector('.drop-area-content').style.display = 'block';
        }
    }

    function previewFiles(files) {
        previewArea.innerHTML = '';
        ([...files]).forEach(previewFile);
    }

    function previewFile(file) {
        let reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onloadend = function() {
            let img = document.createElement('img')
            img.src = reader.result
            img.style.maxWidth = '100px'
            img.style.maxHeight = '100px'
            img.style.margin = '5px'
            previewArea.appendChild(img)
        }
    }

    dropArea.addEventListener('click', function() {
        fileElem.click();
    });

    fileElem.addEventListener('change', function() {
        if (this.files.length > 0) {
            handleFiles(this.files);
        } else {
            showDropAreaIfEmpty();
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(form);
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);
        xhr.upload.onprogress = function(e) {
            if (e.lengthComputable) {
                var percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete + '%';
                progressBar.textContent = percentComplete.toFixed(2) + '%';
                progressBar.setAttribute('aria-valuenow', percentComplete);
                progressBarContainer.style.display = 'block';
            }
        };
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Успешная загрузка
                window.location.href = xhr.responseURL;
            } else {
                // Обработка ошибок
                alert('Произошла ошибка при загрузке.');
            }
        };
        xhr.send(formData);
    });
});