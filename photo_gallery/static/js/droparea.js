document.addEventListener('DOMContentLoaded', function() {
    var dropArea = document.getElementById('drop-area');
    var fileElem = document.getElementById('fileElem');
    var previewArea = document.getElementById('preview-area');
    var form = document.querySelector('form');
    var progressBar = document.getElementById('progress-bar');
    var progressBarContainer = document.getElementById('progress-bar-container');
    var processingMessage = document.createElement('div');
    var dots = document.createElement('span');

    const MAX_FILES = 150; // Максимальное количество файлов
    const MAX_SIZE = 1024 * 1024 * 1024; // 1 ГБ в байтах

    processingMessage.style.textAlign = 'center';
    processingMessage.style.marginTop = '10px';
    processingMessage.style.fontWeight = 'bold';

    function animateDots() {
        let count = 0;
        return setInterval(() => {
            count = (count + 1) % 4;
            dots.textContent = '.'.repeat(count);
        }, 500);
    }

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
        if (files.length > MAX_FILES) {
            alert(`Пожалуйста, выберите не более ${MAX_FILES} файлов.`);
            return;
        }

        let totalSize = 0;
        for (let file of files) {
            totalSize += file.size;
        }

        if (totalSize > MAX_SIZE) {
            alert(`Общий размер файлов не должен превышать 1 ГБ. Текущий размер: ${formatSize(totalSize)}`);
            return;
        }

        fileElem.files = files;
        updateFileInfo(files);
        dropArea.style.display = 'none'; // скрываем область загрузки
    }

    function showDropAreaIfEmpty() {
        if (fileElem.files.length === 0) {
            dropArea.style.display = 'block';
            document.querySelector('.drop-area-content').style.display = 'block';
            previewArea.innerHTML = '';
        }
    }

    function formatSize(bytes) {
        if (bytes === 0) return '0 Байт';
        const k = 1024;
        const sizes = ['Байт', 'КБ', 'МБ', 'ГБ', 'ТБ'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function updateFileInfo(files) {
        let totalSize = 0;
        for (let file of files) {
            totalSize += file.size;
        }
        
        const formattedSize = formatSize(totalSize);
        previewArea.innerHTML = `Выбрано файлов: ${files.length} <br> Размер: ${formattedSize}`;
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

        xhr.upload.onload = function() {
            processingMessage.innerHTML = '<i class="fa fa-spinner fa-pulse fa-2x fa-fw"></i><br>Почти готово! 🚀 <br> Обрабатываем данные...<br><hr>';
            processingMessage.appendChild(dots);
            progressBarContainer.after(processingMessage);
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
        
        xhr.onerror = function() {
            alert('Произошла ошибка при загрузке.');
        };
        
        xhr.send(formData);
    });
});