document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('downloadAllBtn');
    const loadingMessage = document.getElementById('loadingMessage');

    downloadBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        loadingMessage.style.display = 'block';
        
        axios.get(this.href, {
            responseType: 'blob'
        }).then(function(response) {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'photos.zip');
            document.body.appendChild(link);
            link.click();
        }).catch(function(error) {
            console.error('Ошибка при скачивании:', error);
        }).finally(function() {
            loadingMessage.style.display = 'none';
        });
    });
});